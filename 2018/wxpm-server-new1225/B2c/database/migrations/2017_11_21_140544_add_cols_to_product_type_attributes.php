<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddColsToProductTypeAttributes extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('product_type_attributes', function (Blueprint $table) {
            //
            $table->tinyInteger('input_type')->default(0)->comment('输入类型0输入框1选择')->after('name');
            $table->text('values')->comment('可供选择的选项值列表|分割')->after('input_type');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('product_type_attributes', function (Blueprint $table) {
            //
        });
    }
}
