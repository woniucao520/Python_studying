{{-- resources/views/admin/dashboard.blade.php --}}
@push('js')
<script src="/js/bootstrap-treeview.js"></script>
@endpush
@extends('adminlte::page')

@section('title', '商品分类')

@section('content_header')
    {{--<h1>transaction products here</h1>--}}
@stop

@section('content')
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">
                商品分类
            </h3>
        </div>
        <div class="panel-body">
            <div id="tree"></div>
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
@push('js')
<script>
    function getTree(){
        var tree = [
            {
                text: "父级",
                'ss':'bb',
                nodes: [
                    {
                        text: "Child 1",
                        nodes: [
                            {
                                text: "Grandchild 1"
                            },
                            {
                                text: "Grandchild 2"
                            }
                        ]
                    },
                    {
                        text: "Child 2"
                    }
                ]
            },
            {
                text: "Parent 2"
            },
            {
                text: "Parent 3"
            },
            {
                text: "Parent 4"
            },
            {
                text: "Parent 5"
            }
        ];
        return tree;
    }
    $(function(){
        $.ajax({
            method:'get',
            url: '/api/category/categories',
            data: {},
            dataType:'json'
        }).done(function(data){
            $('#tree').treeview({data: data});
        });
    });
</script>
@endpush