@foreach($products as $product)
    <ons-list-item data-id="{{$product->id}}" modifier="chevron" tappable>
        <ons-row>
            <ons-col width="100px"><img src="{{$product->thumb}}" width="100%" height="auto" /> </ons-col>
            <ons-col width="60%">
                <div style="padding-left:5px;display:flex;flex-direction: column;height: 100%;">
                    <div style="flex: 1">商品名:{{$product->name}}</div>
                    <div style="flex: 1">商品价格:{{$product->rmb_price}}</div>
                    <div style="flex:1;position: relative;"><span style="display: inline-block;position: absolute;bottom: 2px">商品编号:{{$product->serial}}</span></div>
                </div>
            </ons-col>
            <ons-col width="10%"></ons-col>
        </ons-row>
    </ons-list-item>
@endforeach