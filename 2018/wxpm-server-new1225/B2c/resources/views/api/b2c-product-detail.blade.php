<div class="product-album-list">
    <ons-carousel fullscreen swipeable auto-scroll overscrollable id="b2-product-detail-carousel">
        @foreach($product->albums as $album)
            <ons-carousel-item>
                <div style="text-align:center;width:100%;height:auto;">
                    <img src="{{$album->url}}" width="100%" height="auto">
                </div>
            </ons-carousel-item>
        @endforeach
    </ons-carousel>

    <div class="dots">
        @for($i=0;$i<count($product->albums);$i++)
            <span id="dot{{$i}}" class="dot" onclick="fn.carousel.swipe('home-carousel',this)">
            &#9679;
        </span>
        @endfor
    </div>
</div>
<ons-row class="b2c-attribute-row">
    <ons-col>{{$product->name}}</ons-col>
</ons-row>
<ons-row class="b2c-attribute-row">
    <ons-col><b>克数:{{$product->gram_price}}g</b></ons-col>
    {{--<ons-col><b><ons-icon icon="fa-cny"></ons-icon>{{$product->rmb_price}}</b></ons-col>--}}
</ons-row>
<ons-row class="b2c-attribute-row">
    <ons-col width="50%">规格:{{$product->specs}}</ons-col>
    <ons-col width="50%">编号:{{$product->serial}}</ons-col>
</ons-row>
<ons-row class="b2c-attribute-row">
    <ons-col width="50%">所需积分:{{$product->bonus_price}}</ons-col>
    <ons-col width="50%">所需虚拟币:{{$product->coin_price}}</ons-col>
</ons-row>
<ons-row class="b2c-attribute-row">
    <ons-col><ons-button id="do-buy-btn" modifier="large">确定购买</ons-button></ons-col>
</ons-row>
<style>
    .b2c-attribute-row{
        padding: 5px;
    }
    .product-album-list{
        position: relative;min-height: 360px;
    }
    .dots {
        text-align: center;
        font-size: 20px;
        color: #fff;
        position: absolute;
        bottom: 20px;
        left: 0;
        right: 0;
    }

    .dots > span {
        cursor: pointer;
    }
</style>