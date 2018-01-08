window.fn.Product = {}

window.fn.Product.setCurrentProduct = function(p_no, name, status){
    localStorage.setItem('wx-current-product-no',p_no);
    localStorage.setItem('wx-current-product-name',name);
    localStorage.setItem('wx-current-product-status', status)
}

window.fn.Product.getCurrentProduct = function(key){
    if(key == 'name')
        return localStorage.getItem('wx-current-product-name');
    else
        return localStorage.getItem('wx-current-product-no');

}

window.fn.Product.ajaxLoadHtml = function(url, target, data){
    //fn.ajaxLoadHtml(url, data, target)
     $.ajax({
        method:'post',
        url: url,
        data: data,
        dataType:'html',
        cache: false
    }).done(function(data){
        $(target).html(data)
    });
}

window.fn.Product.ajaxGetProducts = function(target){

    fn.Product.ajaxLoadHtml('/product/list',target)
}

window.fn.Product.quickValue = function(step, target, max, fixed){
    o_value = Number($(target).val());

    if(o_value <= 0 && step < 0)
        return;

    if(step<0 && o_value<=max){
        $(target).val(max);
        return;
    }

    if(o_value + step <= 0){
        $(target).val(0)
        return;
    }

    value = Number(o_value+step).toFixed(fixed)
    if(max > 0){
        if(step > 0){
            if(value > max){
                value = max;
            }
        }else{
            if(value < max)
                value = max;
        }
    }else{
        value=0
    }

    $(target).val(value)
}

window.fn.Product.doBuy = function(up, dp, mv){
    price = parseFloat($('#exchange-buy #buy-product-price').val());
    qty = parseInt($('#exchange-buy #buy-product-qty').val());

    if(price > up || price < dp){
        ons.notification.alert('价格输入有误!');
        return;
    }

    if(price * qty > mv){
        //TODO checking here
    }

    message = '品名:'+fn.Product.getCurrentProduct('name')+'<br>';
    message += '代码:'+fn.Product.getCurrentProduct()+'<br>';
    message += '价格:'+ price + '<br>';
    message += '数量:'+qty + '<br>';

    message += '确定发出以上委托吗?'

    ons.notification.confirm({'message':message}).then(function(idx){
        if(idx == 1){
            fn.showLoading()

            $.ajax({
                method:'post',
                url: '/user/buy',
                data: {user_id:fn.User.getLoginId(),p_no:fn.Product.getCurrentProduct(),price:price,qty:qty},
                dataType:'json'
            }).done(function(data){
                fn.hideLoading();
                ons.notification.alert(data.msg).then(function(){
                    //fn.Product.reloadBuyPage()
                });

            });
        }
    });
}

window.fn.Product.doSale = function(){
    price = parseFloat($('#exchange-sale #sale-product-price').val());
    qty = parseInt($('#exchange-sale #sale-product-qty').val());

    message = '品名:'+fn.Product.getCurrentProduct('name')+'<br>';
    message += '代码:'+fn.Product.getCurrentProduct()+'<br>';
    message += '价格:'+ price + '<br>';
    message += '数量:'+qty + '<br>';

    message += '确定发出以上委托吗?'


    ons.notification.confirm({'message':message}).then(function(idx){
        if(idx == 1){
            fn.showLoading()

            $.ajax({
                method:'post',
                url: '/user/sale',
                data: {user_id:fn.User.getLoginId(),p_no:fn.Product.getCurrentProduct(),price:price,qty:qty},
                dataType:'json'
            }).done(function(data){
                fn.hideLoading();
                ons.notification.alert(data.msg).then(function(){
                    //fn.Product.reloadSalePage()
                });

            });
        }
    });
}

window.fn.Product.reloadBuyPage = function(){
    fn.Product.ajaxLoadHtml('/product/buy','#exchange-buy-content',{p_no:fn.Product.getCurrentProduct(),user_id:fn.User.getLoginId()});
}

window.fn.Product.reloadSalePage = function(){
    fn.Product.ajaxLoadHtml('/product/sale','#exchange-sale-content',{p_no:fn.Product.getCurrentProduct(),user_id:fn.User.getLoginId()});
}

window.fn.Product.renderDetail = function(target){

    $.ajax({
        method:'post',
        url:'product/detail',
        data:{p_no:fn.Product.getCurrentProduct()},
        dataType:'html'
    }).done(function(data){
        $(target).html(data);

        //setInterval(function(){
            fn.Product.ajaxLoadHtml('/product/detail', '#general-data-container',{p_no:fn.Product.getCurrentProduct(),segment:'general'})
        //},1000);

        //setInterval(function(){
            fn.Product.ajaxLoadHtml('/product/detail', '#sale-buy-delegate-container',{p_no:fn.Product.getCurrentProduct(),segment:'bs5'})
        //},1000);

        fn.Product.drawTimeChart('data-canvas');

        fn.Product.ajaxLoadHtml('/product/detail', '#info-panel-container',{p_no:fn.Product.getCurrentProduct(),segment:'info'})

        });
}

window.fn.Product.switchCanvas = function(show, hide){
    $(show).show();
    $(hide).hide();
}

window.fn.Product.timeChartInit = function(target, x_times, d_price, a_price, d_volume){
    var chartObj = fn.chart(target);

    var x_times = x_times;
    var d_price = d_price;
    var a_price = a_price;
    var d_volume = d_volume;

    var options = {
        baseOption:{
            title:{
                text: '分时'
            },
            tooltips:{},
            legend:{
                data:['成交价','平均价']
            },
            grid: [
                {
                    left: '10%',
                    right: '10%',
                    height: '50%'
                },
                {
                    left: '10%',
                    right: '10%',
                    top: '75%',
                    height: '20%'
                }
            ],
            xAxis:[
                {
                    type:'category',
                    boundaryGap:false,
                    scale:true,
                    data: x_times,
                    axisLine:{
                        lineStyle:{
                            color:'#999'
                        }
                    },
                    axisLabel:{
                        showMaxLabel:true
                    }
                },
                {
                    type:'category',
                    boundaryGap:false,
                    scale: true,
                    gridIndex:1,
                    data: x_times,
                    axisLabel: {show: false},
                    axisLine:{
                        lineStyle:{
                            color:'#999'
                        }
                    }
                }
            ],
            yAxis:[
                {
                    scale:true,
                    splitNumber:5,
                    splitLine:{
                        show:true,
                        lineStyle:{
                            color:'#444'
                            }
                        },
                    axisLine:{
                        lineStyle:{
                            color:'#999'
                        }
                    },
                    min:function(value){
                        return parseFloat(value.min-0.5).toFixed(2);
                    },
                    max:function(value){
                        return parseFloat(value.max+0.1).toFixed(2);
                    }
                },
                {
                    scale:true,
                    splitLine:{show:false},
                    gridIndex:1,
                    splitNumber:2,

                    axisLine:{
                        lineStyle:{
                            color:'#999'
                        }
                    }
                }
            ],
            series:[
                {
                    name:'成交价',
                    type:'line',
                    yAxisIndex:0,
                    data:d_price,
                    smooth:true,
                    lineStyle:{
                        normal:{
                            color:'#fff'
                        }
                    },
                    zlevel:10
                },
                {
                    name:'平均价',
                    type:'line',
                    yAxisIndex:0,
                    data:a_price,
                    smooth:true,
                    lineStyle:{
                        normal:{
                            color:'yellow'
                        }
                    },
                    zlevel:9
                },
                {
                    name:'成交量',
                    type:'bar',
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    data:d_volume,
                    barMaxWidth:15,

                }
            ]
        },
    };

    chartObj.setOption(options)

    return chartObj;
}

window.fn.Product.updateChart = function(chartObj, option){
    chartObj.setOption(option);
}

window.fn.Product.KChartSplitData = function(rawData){
    var categoryData = [];
    var values = []
    var volumes = []
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i]);
        volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1]);
    }
    return {
        categoryData: categoryData,
        values: values,
        volumes: volumes
    };
}

window.fn.Product.calculateMA = function(data, dayCount){
    var result = [];
        for (var i = 0, len = data.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data[i - j][1];
            }
            result.push(sum / dayCount);
        }
        return result;
}

window.fn.Product.KChartInit = function(target,k_data){

    var chartObj = fn.chart(target);

    var upColor = '#ec0000';
    var upBorderColor = '#8A0000';
    var downColor = '#00da3c';
    var downBorderColor = '#008F28';

    function calculateMA(dayCount) {
        var result = [];
        for (var i = 0, len = data0.values.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data0.values[i - j][1];
            }
            result.push(sum / dayCount);
        }
        return result;
    }

    var data0 = fn.Product.KChartSplitData(k_data);

    var options = {
        title:{
            text:'日K',
            left:0
        },

        tooltip:{
            show: true,
            trigger: 'axis',
            axisPointer:{
                type: 'cross'
            },
            formatter: function(param){
                p_one = param[0];
                if(p_one.componentSubType == 'bar'){
                    p_two = param[1];
                    return [
                        p_one.name +'<hr size=1 style="margin: 3px 0">',
                        '开盘:' + p_two.data[1] + '<br/>',
                        '收盘:' + p_two.data[2] + '<br/>',
                        '最低:' + p_two.data[3] + '<br/>',
                        '最高:' + p_two.data[4] + '<hr size=1 style="margin: 3px 0">',
                        '成交量:' + p_one.data[1] + '<br/>',
                    ].join('');
                }else{
                    p_two = param[4];
                    return [
                        p_one.name +'<hr size=1 style="margin: 3px 0">',
                        '开盘:' + p_one.data[1] + '<br/>',
                        '收盘:' + p_one.data[2] + '<br/>',
                        '最低:' + p_one.data[3] + '<br/>',
                        '最高:' + p_one.data[4] + '<hr size=1 style="margin: 3px 0">',
                        '成交量:' + p_two.data[1] + '<br/>',
                    ].join('');
                 }
            },
            /*
            position: function (pos, params, el, elRect, size) {
                var obj = {top: 10};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            }*/
        },
        axisPointer: {
            link: {xAxisIndex: 'all'},
            label: {
                backgroundColor: '#777'
            }
        },
        legend:{
            data:['日K','MA5','MA10','MA20']
        },
        grid:[
            {
                left: '10%',
                right: '8%',
                height: '50%'
            },
            {
                left: '10%',
                right: '8%',
                top: '70%',
                height: '20%'
            }
        ],
        xAxis:[
            {
                type: 'category',
                data: data0.categoryData,
                scale: true,
                boundaryGap: true,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 2,
                min: 'dataMin',
                max: 'dataMax',
                axisLine:{
                            lineStyle:{
                                color:'#999'
                            }
                        }
            },
            {
                type: 'category',
                gridIndex: 1,
                data: data0.categoryData,
                scale: true,
                boundaryGap : true,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                splitNumber: 2,
                min: 'dataMin',
                max: 'dataMax'
            }
        ],
        yAxis:[
            {
                scale: true,
                splitArea:{
                    show: true
                },
                min:0,
                axisLine:{
                            lineStyle:{
                                color:'#999'
                            }
                        }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false}
            }
        ],
        dataZoom:[
            {
                type: 'inside',
                xAxisIndex:[0,1],
                start:50,
                end:100
            },
            {
                show:true,
                type: 'slider',
                xAxisIndex:[0,1],
                y: '90%',
                start: 0,
                end: 100
            }
        ],
        visualMap:{
            show:false,
            seriesIndex: 4,
            dimension:2,
            pieces:[
                {
                    value: 1,
                    color: downColor
                },
                {
                    value: -1,
                    color: upColor
                }
            ]
        },
        series:[
            {
                name: '日K',
                type: 'candlestick',
                data: data0.values,
                itemStyle:{
                    normal:{
                        color: upColor,
                        color0: downColor,
                        borderColor: upBorderColor,
                        borderColor0: downBorderColor
                    }
                },
                barMaxWidth:15,
                markPoint:{
                    label:{
                        normal:{
                            formatter: function(param){
                                return param != null ? parseFloat(param.value).toFixed(2): '';
                            }
                        }
                    },
                    data:[
                        {
                            name: 'XX标点',
                            coord: ['2017-10-23', 2300],
                            value: 2300,
                            itemStyle:{
                                normal:{color: 'rgb(41,60,85)'}
                            }
                        },
                        {
                            name: 'Max',
                            type: 'max',
                            valueDim: 'highest'
                        },
                        {
                            name: 'Min',
                            type: 'min',
                            valueDim: 'lowest'
                        },
                        {
                            name: 'Avg',
                            type: 'average',
                            valueDim: 'close'
                        }
                    ]
                }

            },
            {
                name: 'MA5',
                type: 'line',
                data: fn.Product.calculateMA(data0.values, 5),
                smooth: true,
                lineStyle:{
                    normal:{opacity: 0.5}
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: fn.Product.calculateMA(data0.values, 10),
                smooth: true,
                lineStyle:{
                    normal:{opacity: 0.5}
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: fn.Product.calculateMA(data0.values, 20),
                smooth: true,
                lineStyle:{
                    normal:{opacity: 0.5}
                }
            },
            {
                name: 'Volume',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data0.volumes,
                barMaxWidth:15,

            }
        ]
    };

    $('#'+target).hide();

    chartObj.setOption(options)

    return chartObj;
}

window.fn.Product.setValue = function(obj, value){
    var old_value = $(obj).text();

    if(old_value == '--'&& value == '--')
        return;

    if(parseFloat(old_value) != parseFloat(value)){
        $(obj).addClass('splashBgColor').fadeOut(100);
        $(obj).fadeIn(1000).text(value).removeClass('splashBgColor');
    }
}

window.fn.Product.updateGeneralData = function(data){
    var current_price = $('#trans-product-content #current-price-up');
    var price_delta = $('#trans-product-content #price-delta');
    var price_gains = $("#trans-product-content #price-gains");
    var open_price = $('#trans-product-content #open-price');
    var max_price = $('#trans-product-content #max-price');
    var total_volume = $('#trans-product-content #total-volume');
    var turn = $('#trans-product-content #turn');
    var min_price = $('#trans-product-content #min-price');
    var total_amount = $('#trans-product-content #total-amount');

    fn.Product.setValue(current_price, data.current_price);
    fn.Product.setValue(price_delta, fn.Round(data.delta*1.00,2));
    fn.Product.setValue(price_gains, fn.Round(data.gains*1.00,2)+'%');
    fn.Product.setValue(open_price, fn.Round(data.open_price*1.00,2));
    fn.Product.setValue(max_price, fn.Round(data.max_price*1.00,2));
    fn.Product.setValue(total_volume, data.total_volume);
    fn.Product.setValue(turn, fn.Round(data.turn*1.00,2)+'%');
    fn.Product.setValue(min_price,fn.Round(data.min_price*1.00,2));

    ta = parseFloat(data.total_amount);
    if (ta > 10000){
        fn.Product.setValue(total_amount,fn.Round((ta/10000.00),2)+'万');
    }else{
        fn.Product.setValue(total_amount,fn.Round(ta*1.00,2));
    }

}

window.fn.Product.updateTopFiveSales = function(data, prefix=''){
    var ptarget_prefix = '#s_d_price_';
    var vtarget_prefix = '#s_d_volume_';

    if(data.length == 0){
        for(i=0; i<5; i++){
            pObj = $(prefix + " " + ptarget_prefix+''+i);
            vObj = $(prefix + " " + vtarget_prefix+''+i);

            fn.Product.setValue(pObj, '--');
            fn.Product.setValue(vObj, '--');
        }
    }else{

        for(i=0; i<data.length; i++){
            pObj = $(prefix + " " + ptarget_prefix+''+i);
            vObj = $(prefix + " " + vtarget_prefix+''+i);

            fn.Product.setValue(pObj, data[i][1]);
            fn.Product.setValue(vObj, data[i][2]);
        }
    }
}

window.fn.Product.updateTopFiveBuys = function(data, prefix=''){
    var ptarget_prefix = '#b_d_price_';
    var vtarget_prefix = '#b_d_volume_';

    if(data.length == 0){
        for(i=0; i<5; i++){
            pObj = $(prefix + " " + ptarget_prefix+''+i);
            vObj = $(prefix + " " + vtarget_prefix+''+i);

            fn.Product.setValue(pObj, '--');
            fn.Product.setValue(vObj, '--');
        }
    }else{
        for(i=0; i<data.length; i++){
            pObj = $(prefix + " " + ptarget_prefix+''+i);
            vObj = $(prefix + " " + vtarget_prefix+''+i);

            fn.Product.setValue(pObj, data[i][1]);
            fn.Product.setValue(vObj, data[i][2]);
        }
    }
}