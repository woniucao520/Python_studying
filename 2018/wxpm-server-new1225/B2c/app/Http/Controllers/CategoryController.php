<?php

namespace App\Http\Controllers;

use App\Category;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    //
    public function __construct()
    {
        $this->middleware('auth');
    }

    function generateTree($categories){
        $tree = [];
        foreach($categories as $category){
            if($category->parent_id != 0 && isset($categories[$category->parent_id])){
                $nodes = $categories[$category->parent_id]->nodes ?:[];
                $nodes[] = &$categories[$category->id];
                $categories[$category->parent_id]->nodes = $nodes;
            }else{
                $tree[] = &$categories[$category->id];
            }
        }
        return $tree;
    }

    public function categories(Request $request)
    {
        $categories = Category::all();
        $prepared = [];
        foreach ($categories as $category){
            $category->text = $category->name;
            $prepared[$category->id] = $category;
        }
        $categories = $this->generateTree($prepared);
        return $categories;

    }
}
