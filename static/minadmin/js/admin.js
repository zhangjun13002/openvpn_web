layui.define(['jquery', 'message'],
	function(exports) {
		"use strict";

		var $ = layui.jquery;
        var message = layui.message;

		var body = $('body');
        var container = $("#container");
        var collasped = false;
        var options = Object;
        var configPath = "config.json";

		var Admin = {
            setConfig: function(path) {
                var url = "";
                if ( path === null || path === undefined || path === "") {
                    url = configPath;
                } else {
                    url = path;
                }
                $.ajax({
                    url: url,
                    type: 'get',
                    dataType: 'json',
                    async: false,
                    success: function(value) {
                        options = value;
                    }
                })                				
			},

            render: function() {
                this.renderPage();
                if ( options.msgshow === true ) {
                    this.messageRender(options);
                }                               
            },            

            renderHome: function() {
                var home = $("#homePage");
                var href = home.attr('lay-href');
                var html = this.getContent(href);
                container.html(html);
            },

            renderPage: function () {
                var pageurl = sessionStorage.getItem('pageurl');

                if ( pageurl === null || pageurl === undefined || pageurl === "" ) {
                    this.renderHome();
                } else {                    
                    var html = this.getContent(pageurl);
                    container.html(html);                                       
                }                
            },

            messageRender: function(options) {
                var params = {
                    elem: ".notice-message",
                    url: null,
                    height: null
                };
                if ( options.msg ) {
                    params.url = options.msg.url;
                    params.height = options.msg.height;   
                }
                message.render(params);
            },

            getContent: function(url) {
                var data = "";
                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'html',
                    async: false,
                    success: function(value) {
                        data = value;
                    },
                    error: function(xhr, status) {
                        return layer.msg('Status:' + xhr.status);
                    }
                })
                return data;
            }                                
		};

        body.on('click', '*[lay-href]', function(){
            var href = $(this).attr('lay-href');
            if (href === null || href === undefined || href === '') {
                Admin.renderHome();
            } else {
                var html = Admin.getContent(href);
                container.html(html);
                sessionStorage.setItem('pageurl', href);
            }                  
        });

        function collaspe() {
            var left = $(".layui-side");
            var right = $(".layui-body");
            if ( collasped === true ) {                    
                left.removeClass("nav-collaspe");
                right.removeClass("nav-collaspe");
                left.addClass("nav-collaspe-show");
                right.addClass("nav-collaspe-show");
                collasped = false;
            } else {
                left.removeClass("nav-collaspe-show");
                right.removeClass("nav-collaspe-show");
                left.addClass("nav-collaspe");
                right.addClass("nav-collaspe");
                collasped = true;
            }
        };

        function refresh() {
            Admin.renderPage();
        };

        $("#btnCollaspe").click(function() {
            collaspe();
        })

        $("#btnRefresh").click(function() {
            refresh();
        })

		exports('admin', Admin);
	}
)
