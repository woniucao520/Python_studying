{{-- resources/views/admin/dashboard.blade.php --}}

@extends('adminlte::page')

@section('title', '交易商品')

@section('content_header')
    {{--<h1>transaction products here</h1>--}}
@stop

@section('content')
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">
                交易商品
            </h3>
        </div>
        <div class="panel-body">
            <table class="table table-bordered">
                {{--<caption>边框表格布局</caption>--}}
                <thead>
                <tr>
                    <th>pub_id</th>
                    <th>p_no</th>
                    <th>name</th>
                    <th>issue_price</th>
                    <th>unit</th>
                    <th>qty</th>
                    <th>turn_qty</th>
                    <th>last_price</th>
                    <th>bonus_ratio</th>
                    <th>ex_from</th>
                    <th>ex_end</th>
                    <th>status</th>
                </tr>
                </thead>
                <tbody>
                @foreach($products as $product)
                    <tr>
                        <td>{{$product->pub_id}}</td>
                        <td>{{$product->p_no}}</td>
                        <td>{{$product->name}}</td>
                        <td>{{$product->issue_price}}</td>
                        <td>{{$product->unit}}</td>
                        <td>{{$product->qty}}</td>
                        <td>{{$product->turn_qty}}</td>
                        <td>{{$product->last_price}}</td>
                        <td>{{$product->bonus_ratio}}</td>
                        <td>{{$product->ex_from}}</td>
                        <td>{{$product->ex_end}}</td>
                        <td>{{$product->status}}</td>
                    </tr>
                @endforeach
                </tbody>
            </table>
        </div>
    </div>
{{--    <div>{{$products->links()}}</div>--}}
@stop

@section('css')
    <link rel="stylesheet" href="/css/admin_custom.css">
@stop

@section('js')
    <script> console.log('Hi!'); </script>
@stop