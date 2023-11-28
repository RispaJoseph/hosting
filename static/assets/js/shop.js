(function ($) {
  "use strict";
  /*Product Details*/
  var productDetails = function () {
    $(".product-image-slider").slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      fade: false,
      asNavFor: ".slider-nav-thumbnails",
    });

    $(".slider-nav-thumbnails").slick({
      slidesToShow: 5,
      slidesToScroll: 1,
      asNavFor: ".product-image-slider",
      dots: false,
      focusOnSelect: true,
      prevArrow:
        '<button type="button" class="slick-prev"><i class="fi-rs-angle-left"></i></button>',
      nextArrow:
        '<button type="button" class="slick-next"><i class="fi-rs-angle-right"></i></button>',
    });

    // Remove active class from all thumbnail slides
    $(".slider-nav-thumbnails .slick-slide").removeClass("slick-active");

    // Set active class to first thumbnail slides
    $(".slider-nav-thumbnails .slick-slide").eq(0).addClass("slick-active");

    // On before slide change match active thumbnail to current slide
    $(".product-image-slider").on(
      "beforeChange",
      function (event, slick, currentSlide, nextSlide) {
        var mySlideNumber = nextSlide;
        $(".slider-nav-thumbnails .slick-slide").removeClass("slick-active");
        $(".slider-nav-thumbnails .slick-slide")
          .eq(mySlideNumber)
          .addClass("slick-active");
      }
    );

    $(".product-image-slider").on(
      "beforeChange",
      function (event, slick, currentSlide, nextSlide) {
        var img = $(slick.$slides[nextSlide]).find("img");
        $(".zoomWindowContainer,.zoomContainer").remove();
        $(img).elevateZoom({
          zoomType: "inner",
          cursor: "crosshair",
          zoomWindowFadeIn: 500,
          zoomWindowFadeOut: 750,
        });
      }
    );
    //Elevate Zoom
    if ($(".product-image-slider").length) {
      $(".product-image-slider .slick-active img").elevateZoom({
        zoomType: "inner",
        cursor: "crosshair",
        zoomWindowFadeIn: 500,
        zoomWindowFadeOut: 750,
      });
    }
    //Filter color/Size
    $(".list-filter").each(function () {
      $(this)
        .find("a")
        .on("click", function (event) {
          event.preventDefault();
          $(this).parent().siblings().removeClass("active");
          $(this).parent().toggleClass("active");
          $(this)
            .parents(".attr-detail")
            .find(".current-size")
            .text($(this).text());
          $(this)
            .parents(".attr-detail")
            .find(".current-color")
            .text($(this).attr("data-color"));
        });
    });
    //Qty Up-Down
    $(".detail-qty").each(function () {
      var qtyval = parseInt($(this).find(".qty-val").text(), 10);
      $(".qty-up").on("click", function (event) {
        event.preventDefault();
        qtyval = qtyval + 1;
        $(this).prev().text(qtyval);
      });
      $(".qty-down").on("click", function (event) {
        event.preventDefault();
        qtyval = qtyval - 1;
        if (qtyval > 1) {
          $(this).next().text(qtyval);
        } else {
          qtyval = 1;
          $(this).next().text(qtyval);
        }
      });
    });

    $(".dropdown-menu .cart_list").on("click", function (event) {
      event.stopPropagation();
    });
  };
  /* WOW active */
  new WOW().init();

  //Load functions
  $(document).ready(function () {
    productDetails();
  });
})(jQuery);





// Add to cart functionality
$("#add-to-cart-btn").on("click", function () 
{
  // let quantity = $("input[name='product-quantity']").val();
  let quantity = $("#product-quantity").val();
  let product_title = $(".product-title").val();
  let product_id = $(".product-id").val();
  let product_price = $(".current-product-price1").text();

  // let product_price = $(".product-price").text();
  // console.log("Price:", product_price);
  // let product_image = $(".product-image-slider").val();
  // let product_pid = $(".product-id").val();

  let product_image = $(".product-image-sliderr img:first").attr("src");
  // let product_pid = $(".product-image-sliderr figure:first").data("pid");
  let product_pid = $(".product-pid").val();

  let this_val = $(this);


  console.log("Quantity:", quantity);
  console.log("Title:", product_title);
  console.log("Price:", product_price);
  console.log("ID:", product_id);
  console.log("PID:",product_pid);
  console.log("Image:",product_image);
  console.log("Current Element :", this_val);

  $.ajax({
    url: "/add_to_cart/",
    data: {
      id: product_id,
      pid: product_pid,
      image: product_image,
      qty: quantity,
      title: product_title,
      price: product_price,
    },
    dataType: "json",
    beforeSend: function () {
      console.log("Adding Product to Cart...");
    },
    success: function (res) {
      this_val.html("Item added to cart"); // Update button text
      console.log("Added Product to cart!");
      $(".cart-items-count").text(res.totalcartitems)
    },
    error: function (err) {
      console.error("Error adding product to cart:", err);
    },
  });
});



$(".delete-product").on("click", function(){

  let product_id = $(this).attr("data-product")
  let this_val = $(this)

  console.log("Product ID:", product_id);
  $.ajax({
      url: "/delete-from-cart",
      data: {
        "id": product_id
      },
      dataType: "json",
      beforeSend: function(){
        this_val.hide()
      },
      success: function(response){
        this_val.show()
        $("#cart-list").html(response.data)
      }
  })
})



// $(".update-product").on("click", function(){

//   let product_id = $(this).attr("data-product")
//   let this_val = $(this)
//   // let product_quantity = $(".product-qty-" + product_id)
//   let product_quantity = $(".product-qty-" + product_id).val();
//   console.log("Product ID:", product_id);
//   console.log("Product QTY:", product_quantity).val();
//   $.ajax({
//       url: "/update-cart",
//       data: {
//         "id": product_id,
//         "qty": product_quantity,
//       },
//       dataType: "json",
//       beforeSend: function(){
//         this_val.hide()
//       },
//       success: function(response){
//         this_val.show()
//         $("#cart-list").html(response.data)
//       }
//   })
// })





$(".update-product").on("click", function(){
  let product_id = $(this).attr("data-product");
  let this_val = $(this);
  let product_quantity = $(".product-qty-" + product_id).val();

  console.log("Product ID:", product_id);
  console.log("Product QTY:", product_quantity);

  $.ajax({
      url: "/update-cart",
      data: {
        "id": product_id,
        "qty": product_quantity,
      },
      dataType: "json",
      beforeSend: function(){
        this_val.hide()
      },
      success: function(response){
        this_val.show();
        $("#cart-list").html(response.data);
      }
  });
});
