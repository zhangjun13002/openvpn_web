(function (root, factory) {
    if (typeof exports === "object") {
        module.exports = exports = factory();
    } else if (typeof define === "function" && define.amd) {
        define([], factory);
    } else {
        root.Utils = factory();
    }
})(this, function () {
    if ( typeof jQuery == "undefined" ) {
        var head = document.getElementsByTagName("head")[0];
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "https://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.11.3.min.js";
        script.onload = script.onreadystatechange = function () {
            if (!this.readyState || this.readyState == "loaded" || this.readyState == "complete") {
                script.onload = script.onreadystatechange = null;
                head.removeChild(script);
            }
        };
        head.appendChild(script);
    }

    var Utils = (function () {
        var U = {
            encrypt: function (text) {
                var encrypted = "";
                $.ajax({
                    type: "GET",
                    url: "/key",
                    async: false,
                    success: function (resp, textStatus) {
                        var crypt = new JSEncrypt();
                        crypt.setPublicKey(resp);
                        encrypted = crypt.encrypt(text);
                    },
                    error: function (resp, textStatus) {
                        layer.msg("获取key失败");
                    },
                });
                return encrypted;
            },
        };
        return U;
    })();

    return Utils;
});
