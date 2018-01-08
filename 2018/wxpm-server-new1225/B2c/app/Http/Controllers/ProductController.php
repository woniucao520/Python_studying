<?php

namespace App\Http\Controllers;

use App\Category;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    //
    public function __construct()
    {
        $this->middleware('auth');
    }

    public function _list()
    {
        return view('product.list');
    }

    public function categories()
    {
        $categories = Category::all();
        return view('product.categories', compact('categories'));
    }

    public function types()
    {
        return view('product.types');
    }

    public function brands()
    {
        return view('product.brands');
    }
}
