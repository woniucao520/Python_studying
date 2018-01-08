<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateB2cProductCategories extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('product_categories', function (Blueprint $table) {
            $table->increments('id');
            $table->string('name')->nullable()->default('')->comment('分类名称');
            $table->integer('parent_id')->comment('父级分类')->default(0);
            $table->integer('sort_order')->default(0)->comment('排序值越大越靠前');
            $table->string('measure_unit', 300)->default('件')->comment('计量单位');
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
        Schema::dropIfExists('product_categories');
    }
}
