<?php

namespace App\Http\Controllers;

use App\Product;
use Illuminate\Http\Request;

class ApiController extends Controller
{
    public function __construct()
    {
        $this->middleware('orignFree');
    }
    //
    public function products(Request $request)
    {
        $page_size = $request->input('page_size');
        $products = Product::paginate($page_size);
        foreach ($products as $product){
            $product->thumb = config('app.url').$product->thumb;
        }
        $html = view()->make('api.b2c-product-list', compact('products'))->render();
        return ['last_page'=>$products->toArray()['last_page'], 'html'=>$html];
    }

    public function productDetail(Request $request, $id)
    {
        $product = Product::with('albums')->find($id);
        foreach ($product->albums as $album){
            $album->url = config('app.url').$album->url;
        }
        return view('api.b2c-product-detail', compact('product'));
    }
}
