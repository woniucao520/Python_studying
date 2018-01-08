/*Socket Process from here*/
window.fn.socket = $.simpleWebSocket({url:'ws://192.168.154.128:8887/transaction'})
//window.fn.socket = $.simpleWebSocket({url:'ws://wx.zgwmyz.com:8887/transaction'})


window.fn.socket.startRequestTimer = function(cmd, interval){
    console.log('try to start requesting timer...')
    interval  = 2000;
    var timer = window.setInterval(function(){
        if(fn.socket.isConnected())
            fn.socket.send(cmd);
        else
            console.log('websocket is not connected and trying to connect');
            //fn.socket.connect();
    }, interval);

    return timer;
}

window.fn.socket.stopRequestTimer = function(timer){
    console.log('try to stop requesting timer...')
    window.clearInterval(timer);
}

fn.socket.Command = {}

fn.socket.Command.Broadcast = 'CMD_BROADCAST';
fn.socket.Command.ProductList = 'CMD_PRODUCT_LIST';
fn.socket.Command.ProductDetail = 'CMD_PRODUCT_DETAIL';
fn.socket.Command.DealTopFive = 'CMD_DEAL_TOP_5';
fn.socket.Command.UserBuy = 'CMD_USER_BUY';
fn.socket.Command.UserSale = 'CMD_USER_SALE';
fn.socket.Command.UserAssets = 'CMD_USER_ASSETS';

fn.socket.Command.encode = function(cmd, args){
    return JSON.stringify({cmd:cmd,args:args})
}
/***
fn.socket.listen(function(message){
    console.log(message);
    var obj = JSON.parse(message);
    var cmd = obj.cmd
    var args = obj.args

    if(cmd == fn.socket.Command.Broadcast){
        ons.notification.alert(args);
    }

    topPage = fn.appNavigator().topPage.id;

    if(cmd == fn.socket.Command.ProductList){
        if(topPage == 'transaction'){

        }
    }

    if(cmd == fn.socket.Command.ProductDetail){
        if(topPage == 'trans-product'){

        }
    }

    if(cmd == fn.socket.Command.UserBuy){
        if(topPage == 'exchange'){

        }
    }

    if(cmd == fn.socket.Command.UserSale){
        if(topPage == 'exchange'){

        }
    }

    if(cmd == fn.socket.Command.UserAssets){
        if(topPage == 'exchange'){

        }
    }

});
***/