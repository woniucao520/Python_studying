<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddColsToProducts extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('products', function (Blueprint $table) {
            //
            $table->integer('wxpm_product_id')->after('wxpm_category_id')->comment('对应交易商品的编号')->nullable();
            $table->integer('total_release_times')->after('wxpm_product_id')->default(10);
            $table->integer('equal_to_hands')->default(0)->comment('等价于对应商品的手数');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('products', function (Blueprint $table) {
            //
        });
    }
}
