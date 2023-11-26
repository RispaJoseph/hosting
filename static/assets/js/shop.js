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
  let product_price = $("#current-product-price").text();
  let this_val = $(this);

  console.log("Quantity:", quantity);
  console.log("Title:", product_title);
  console.log("Price:", product_price);
  console.log("ID:", product_id);
  console.log("Current Element :", this_val);

  $.ajax({
    url: "/add_to_cart/",
    data: {
      id: product_id,
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
