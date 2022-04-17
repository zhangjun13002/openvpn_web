layui.define(['jquery'],
	function(exports) {
		"use strict";

		var $ = layui.jquery;

		var Message = {
            render: function(params) {
                var option = {
                    elem: params.elem,
                    url: params.url ? params.url : null,
                    height: params.height ? params.height : "300px",
                    data: null,
                };

                if (option.url != null) {
                    option.data = this.getData(option.url);
                }
                var msghtml = this.createHtml(option);
                $(option.elem).html(msghtml); 
            },

            getData: function (url) {
                var data = "";
                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'json',
                    async: false,
                    success: function(value) {
                        data = value;
                    },
                    error: function(xhr, status) {
                        return layer.msg('获取消息错误:' + xhr.status);
                    }
                })
                return data;
            },

            createHtml: function(params) {
                var count = 0;
                var msghtml = '<div class="layui-nav-item">' +
                    '<a href="javascript:;" class="notice layui-icon layui-icon-notice"><span class="layui-badge-dot"></a>' +
                    '<div class="layui-nav-child layui-anim layui-anim-scale minadmin-notice" style="margin-top: 0px;left: -200px;">';

                if ( params.data && params.data.count ) {
                    count = params.data.count;
                }
                var msghtmlTitle = '<div class="layui-layer-title">' +
                                  '<div class="minadmin-notice-header">消息</div>' + 
                                  '<div class="minadmin-notice-count">共 ' + count + ' 条</div></div>';
                var msghtmlContent = '<div class="layui-layer-content" style="height: '+ params.height +';overflow-x: hidden;">';
                
                if ( params.data && params.data.msg ) {
                    $.each(params.data.msg, function(i, item) {
                        msghtmlContent += '<div class="minadmin-notice-item" notice-title="' + item.title + '" notice-id="' + item.id + '">' +
                            '<div class="minadmin-notice-icon"><img src="' + item.icon + '"/></div>' +
                            '<div class="minadmin-notice-title">' + item.title + '</div>'+
                            '<div class="minadmin-notice-end">' + item.time + '</div>' +
                            '</div>';
                    })
                } else {
                    msghtmlContent += '<div class="minadmin-notice-item" notice-title="" notice-id="">' +
                            '<div class="minadmin-notice-icon"><i class="layui-icon layui-icon-dialogue" style="font-size:33px;color:#C3DE68;"></i></div>' +
                            '<div class="minadmin-notice-title">没有消息！</div>'+
                            '<div class="minadmin-notice-end"></div>' +
                            '</div>';
                }
                msghtml += msghtmlTitle;
                msghtml += msghtmlContent;
                msghtml += '</div></div></div>';
                return msghtml;
            }
		};

		exports('message', Message);
	}
)