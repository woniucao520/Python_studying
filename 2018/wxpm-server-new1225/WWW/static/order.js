window.fn.Order = {}

var OrderStatusPending = 0  // 埋单
var OrderStatusCommitted = 1  // 提交success
var OrderStatusFinished = 2  // 完成
var OrderStatusClosed = 3  // 撤单
var OrderStatusPartialFinished = 4  // 部成
var OrderStatusPartialClosed = 5 //部撤

window.fn.Order.statusLabel = function(s){
    if(s == OrderStatusPending)
        return '埋单';
    if(s == OrderStatusCommitted)
        return '发布';

    if(s == OrderStatusFinished)
        return '完成';

    if(s == OrderStatusClosed)
        return '撤单';

    if(s == OrderStatusPartialFinished)
        return '部成';

    if(s == OrderStatusPartialClosed)
        return '部撤';
}

window.fn.Order.loadOrders = function(){
    fn.Product.ajaxLoadHtml('/product/order','#exchange-order-content',{user_id:fn.User.getLoginId()});
}

window.fn.Order.cancel = function(oid, status){
    if(status == OrderStatusFinished || status == OrderStatusClosed || status == OrderStatusPartialClosed)
        return;

    ons.notification.confirm({'message':'确定要撤销委托吗?'}).then(function(idx){
        if(idx == 1){
            fn.showLoading()

            $.ajax({
                method:'post',
                url: '/order/cancel',
                data: {user_id:fn.User.getLoginId(),oid:oid},
                dataType:'json'
            }).done(function(data){
                fn.hideLoading();
                ons.notification.alert(data.msg).then(function(){
                    fn.Order.loadOrders();
                });

            });
        }
    });
}