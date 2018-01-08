<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use App\Album;

class Product extends Model
{
    //
    protected $table = 'products';

    public function albums()
    {
        return $this->hasMany(Album::class,'product_id','id');
    }
}
