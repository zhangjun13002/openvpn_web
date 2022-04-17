#!/bin/bash

username=$1
capass="123456"
curdir=$(cd $(dirname $0); pwd)
cd $curdir

vpnconf="client
dev tun
proto tcp-client
remote myvpn.org 1194

allow-recursive-routing

resolv-retry infinite
nobind
persist-key
persist-tun

remote-cert-tls server
auth-user-pass
auth-nocache

cipher AES-256-CBC
auth SHA512
tls-version-min 1.2
tls-cipher TLS-DHE-RSA-WITH-AES-256-GCM-SHA384:TLS-DHE-RSA-WITH-AES-128-GCM-SHA256:TLS-DHE-RSA-WITH-AES-256-CBC-SHA:TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA:TLS-DHE-RSA-WITH-AES-128-CBC-SHA:TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA

comp-lzo
compress 'lz4'
verb 3
mute 20
"

[ -f "pki/issued/${username}.crt" ] && rm -f pki/issued/${username}.crt
[ -f "pki/private/${username}.key" ] && rm -f pki/private/${username}.key
[ -f "pki/reqs/${username}.req" ] && rm -f pki/reqs/${username}.req


/usr/bin/expect <<-EOF
spawn ./easyrsa build-client-full $username nopass
expect {
   "*ca.key:" {
      send "${capass}\r"
   }
}
expect eof
EOF

[ ! -f "pki/issued/${username}.crt" ] &&  exit -1

CA=$(cat pki/ca.crt)
CERT=$(cat pki/issued/${username}.crt | sed -n '/^-----BEGIN/,/^-----END/p')
KEY=$(cat pki/private/${username}.key)
TA=$(cat /etc/openvpn/server/ta.key)

echo -e "${vpnconf}\n<ca>\n"${CA}"\n</ca>\n<cert>\n"${CERT}"\n</cert>\n<key>\n"${KEY}"\n</key>\n<tls-crypt>\n"${TA}"\n</tls-crypt>" > $username.ovpn
sed -i 's/-----BEGIN CERTIFICATE-----/-----BEGIN CERTIFICATE-----\n/g' $username.ovpn
sed -i 's/-----END CERTIFICATE-----/\n-----END CERTIFICATE-----/g' $username.ovpn
sed -i 's/-----BEGIN PRIVATE KEY-----/-----BEGIN PRIVATE KEY-----\n/g' $username.ovpn
sed -i 's/-----END PRIVATE KEY-----/\n-----END PRIVATE KEY-----/g' $username.ovpn
sed -i 's/-----BEGIN OpenVPN Static key V1-----/\n-----BEGIN OpenVPN Static key V1-----\n/g' $username.ovpn
sed -i 's/-----END OpenVPN Static key V1-----/\n-----END OpenVPN Static key V1-----/g' $username.ovpn

rm -f pki/issued/${username}.crt
rm -f pki/private/${username}.key
rm -f pki/reqs/${username}.req
rm -f pki/certs_by_serial/*.pem
