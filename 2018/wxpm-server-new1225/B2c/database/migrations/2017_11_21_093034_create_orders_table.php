<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateOrdersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->increments('id');
            $table->string('serial', 100)->default('')->nullable();
            //
            $table->tinyInteger('status')->comment('0已下单1已付款2已发货(实物)3分批转化中4已取消')->default('0');
            $table->integer('product_amount')->comment('产品数量')->default(0);
            $table->string('pay_method',100)->comment('[rmb:人民币 coin:虚拟币 bonus:积分 gram:克]');
            $table->decimal('rmb_paid')->comment('人民币付款数量');
            $table->decimal('coin_paid')->comment('虚拟币付款数量');
            $table->decimal('bonus_paid')->comment('积分付款数量');
            $table->decimal('gram_paid')->comment('克付款数量');
            $table->smallInteger('country')->default(0);
            $table->smallInteger('province')->default(0);
            $table->smallInteger('city')->default(0);
            $table->smallInteger('district')->default(0);
            $table->string('address')->default(0);
            $table->string('zipcode')->default('');
            $table->string('phone')->default('');
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
        Schema::dropIfExists('orders');
    }
}
