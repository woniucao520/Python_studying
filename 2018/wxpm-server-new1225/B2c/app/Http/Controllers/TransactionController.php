<?php

namespace App\Http\Controllers;

use App\Transaction\Product;
use Illuminate\Http\Request;
use GuzzleHttp\Client;

class TransactionController extends Controller
{
    //
    public function __construct()
    {
        $this->middleware('auth');
    }

    public function products()
    {
        $client = new Client();
        $res = $client->request('POST', 'http://127.0.0.1:8887/api/transaction/products');
//            [
//            'form_params' => [
//                'client_id' => 'test_id',
//                'secret' => 'test_secret',
//            ]
//        ]
        $result= $res->getBody()->getContents();
        $products = json_decode($result);
        //$products = Product::paginate(10);
        return view('transaction.products', compact('products'));
    }
}
