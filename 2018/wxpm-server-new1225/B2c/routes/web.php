<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
//    return view('welcome');
    return redirect('/login');
});

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
Route::get('product/list', 'ProductController@_list');
Route::get('product/categories', 'ProductController@categories');
Route::get('product/types', 'ProductController@types');
Route::get('product/brands', 'ProductController@brands');

//-------------------transaction-------------------------
Route::get('transaction/products', 'TransactionController@products');


//-------------------   api   ---------------------------

Route::get('/b2c/api/products', 'ApiController@products');
Route::get('/b2c/api/product/{id}', 'ApiController@productDetail');

//-------------------   api     ------------------

Route::get('/api/category/categories', 'CategoryController@categories');