
window.fn = {};

window.fn.ajaxLoadHtml = function(url, data, target){
    $.ajax({
        method:'post',
        url: url,
        data: data,
        dataType:'html'
    }).done(function(data){
        $(target).html(data)
    });
}

/*Page process from here*/
window.fn.appNavigator = function(){
    return document.getElementById('appNavigator');
}

window.fn.pushPage = function(page,anim){
    if(anim){
        document.getElementById('appNavigator').pushPage(page.id, {data: {title:page.title}, animation: anim});
    }else{
        document.getElementById('appNavigator').pushPage(page.id, {data: {title:page.title}});
    }
}


window.fn.open = function(){
    var menu = document.getElementById('menu');
    menu.open();
}

window.fn.load = function(page){

    var menu = document.getElementById('menu');
    var appNavigator = document.getElementById('appNavigator');

     menu.close();
     fn.checkLogin();

    appNavigator.resetToPage(page,{animation:'fade'}).then(menu.close.bind(menu));
}


window.fn.load_ex = function(page, tabTarget, tabIndex){
    window.fn.load(page)
    localStorage.setItem(tabTarget, tabIndex)
}

/*User Process from here*/
window.fn.logout = function(){
    var menu = document.getElementById('menu');
    ons.notification.confirm({'message':'确定要退出吗?'}).then(function(idx){
        if(idx == 1){
            localStorage.removeItem('wx-user-name');
            localStorage.removeItem('wx-user-id');
            fn.load('user-login.html');
        }
    }).then(menu.close.bind(menu));
}

// window.fn.checkLogin = function(){
//     if(!fn.get_current_user()){
//         fn.pushPage({id:'user-login.html','title':'Login'});
//     }
// }

window.fn.checkLogin = function(){
    if(!fn.get_current_user()){
        fn.pushPage({id:'ajax-login.html','title':'Login'});
    }
}



window.fn.get_current_user  = function(){
    var username = localStorage.getItem('wx-user-name');
    var userid = localStorage.getItem('wx-user-id');

    if(!username || !userid){
        return false;
    }

    return userid;
}

window.fn.scanCode = function(){
    return;
}

window.fn.showWalletActionSheet = function(){
    ons.openActionSheet(
        {
            cancelable: true,
            buttons: [
                '充值记录',
                '出金记录',
                '取消'
            ]
        }
    ).then(
        function(index){
            console.log('index:',index);
            if(index==0){
                fn.load('user-deposit-history.html');
            }

            if(index==1){
                fn.load('user-withdraw-history.html')
            }
        });
}


/*Chart process from here*/
window.fn.chart = function(target,option){
    var canvas = document.getElementById(target);
    $(canvas).show();
    var myChart = echarts.init(canvas);
    myChart.clear();
    if(option)
        myChart.setOption(option);
    return myChart;
}

/*QRCode process from here*/
window.fn.qrcode = function(target){
    var el = document.getElementById(target);
        $(el).children().remove();

    var qrcode = new QRCode(el, {
            text: 'http://' + window.location.host + '/?referrer=' + localStorage.getItem('wx-user-id'),
            width: 128,
            height: 128,
            colorDark : "#000000",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.H
        });

}

window.fn.showLoading = function(){
    var modal = document.querySelector('ons-modal');
    modal.show();
}

window.fn.hideLoading = function(){
    var modal = document.querySelector('ons-modal');
    modal.hide();
}

window.fn.toggleActiveTab = function(e, cls){
    $(e).siblings().removeClass(cls);
    $(e).addClass(cls)
}

window.fn.Round = function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}


/*global functions*/
$(document).ready(function(){
    ons.disableDeviceBackButtonHandler();
    ons.enableDeviceBackButtonHandler();

    ons.setDefaultDeviceBackButtonListener(function(event){
        alert('exit app?')
    });
});
