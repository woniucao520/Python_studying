<?php

namespace App\Transaction;

use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    //
    protected $table = 'wx_product';
    protected $connection = 'mysql_transaction';
}
