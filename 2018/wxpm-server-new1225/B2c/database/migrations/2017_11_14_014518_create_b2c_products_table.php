<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateB2cProductsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('products', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name')->comment('产品名')->nullable();
            $table->decimal('rmb_price', 10, 2)->comment('购买价格:人民币部分')->default(0.00)->nullable();
            $table->decimal('coin_price', 10, 2)->comment('购买价格:虚拟币部分')->default(0.00)->nullable();
            $table->decimal('bonus_price', 10, 2)->comment('购买价格:积分部分')->default(0.00)->nullable();
            $table->decimal('gram_price', 10, 2)->comment('购买价格:克部分')->default(0.00)->nullable();
            $table->integer('stock')->comment('库存数')->default(0)->nullable();
            $table->string('serial', 100)->comment('序列号')->default('')->nullable();
            $table->string('thumb')->comment('缩略图')->default('')->nullable();
            $table->longText('detail')->comment('商品详情');
            $table->tinyInteger('is_on_sale')->comment('是否在售0否1是')->default(1);
            $table->integer('type_id')->comment('商品类型分类')->nullable();
            $table->integer('category_id')->comment('商品分类')->nullable();
            $table->integer('wxpm_category_id')->comment('购买范围分类');
            $table->integer('brand_id')->comment('商品品牌')->nullable();
            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('products');
    }
}
