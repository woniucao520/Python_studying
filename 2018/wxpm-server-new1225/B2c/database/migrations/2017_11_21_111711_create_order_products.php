<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateOrderProducts extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('order_products', function (Blueprint $table) {
            $table->increments('id');
            $table->integer('order_id')->comment('订单编号');
            $table->integer('product_id')->comment('商品编号');
            $table->string('product_name')->comment('商品名称');
            $table->decimal('rmb_price', 10, 2)->comment('商品价格');
            $table->decimal('coin_price', 10, 2)->comment('虚拟币价格');
            $table->decimal('bonus_price', 10, 2)->comment('积分价格');
            $table->decimal('gram_price', 10, 2)->comment('克价格');
            $table->string('product_serial')->comment('商品sn编号')->nullable();
            $table->string('product_attribute_values')->comment('属性值文字|分割')->nullable();
            $table->string('product_attribute_ids')->comment('属性值编号|分割')->nullable();
            $table->integer('product_number')->comment('数量');
            //
            $table->tinyInteger('deliver_type')->default(2)->comment('交付方式1实物2分批转化为货');

            $table->integer('already_release_times')->default(0)->comment('如果分批释放:已经释放的次数');
            $table->integer('total_release_times')->default(0)->comment('如果分批释放:分批释放的次数');
            $table->integer('equal_to_hands')->default(0)->comment('等价于对应商品的手数');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('order_products');
    }
}
