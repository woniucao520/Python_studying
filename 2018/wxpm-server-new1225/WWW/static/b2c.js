window.b2c = {

    base_url: 'http://127.0.0.1:8000',

    setStorage(key, value){
        let _b2c = localStorage.getItem('_b2c');
        if(!_b2c){
            _b2c = {};
        }else{
            _b2c = JSON.parse(_b2c);
        }
        _b2c[key] = value;
        localStorage.setItem('_b2c', JSON.stringify(_b2c));
    },

    getStorage(key){
        let _b2c = localStorage.getItem('_b2c');
        if(!_b2c){
            return '';
        }else{
            _b2c = JSON.parse(_b2c);
            return _b2c[key]
        }
    }
}

window.b2c.listPage = {

    el:"#b2c-product-list",
    page_size:10,

    init(){
        this.loadPage(1);
    },
    loadPage(page){
        let _this = this;
        $.ajax({
                method:'get',
                url: b2c.base_url + '/b2c/api/products',
                data: {page: page, page_size: _this.page_size},
                dataType:'json'
            }).done(function(data){
                b2c.setStorage('listPage.total_page', data.last_page);
                $(_this.el).append($(data.html));
                //bind click event
                $(_this.el).find(".list-item").unbind().bind('click', function(){
                    const product_id = $(this).attr('data-id');
                    b2c.setStorage('listPage.current_product_id', product_id);
                    fn.load('b2c-product-detail.html');
                });
            });
    },

    loadMoreProducts(done){
          setTimeout(() => {
              const total_page = b2c.getStorage('listPage.total_page')
              const list_length = $(this.el).children().length
              const page = Math.ceil(list_length / this.page_size)
              if( page >= total_page){
                  $(this.el).parent().find(".after-list").html("<p class='center'>无更多商品</p>");
              }else{
                  this.loadPage(page+1)
              }
              done();
          }, 300)
    }
}




window.b2c.productDetail = {
    load(callback){
        const current_product_id = b2c.getStorage('listPage.current_product_id')
        $.ajax({
            method: 'get',
            url:b2c.base_url + '/b2c/api/product/'+current_product_id,
            dataType:'html'
        }).done(function(data){
            callback(data)
        });
    }
}
// window.b2c.listPage = listPage
// window.b2c.productDetail = productDetail