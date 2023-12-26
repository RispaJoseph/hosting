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








$("#add-to-cart-btn").on("click", function () {
  let this_val = $(this);
  let index = this_val.attr("data-index");
  let quantity = $(".product-quantity-" + index).val();

  let product_title = $(".product-title-" + index).val();
  let product_id = $(".product-id-" + index).val();
  let product_price = parseFloat($(".current-product-price-" + index).text());
  let product_pid = $(".product-pid-" + index).val();
  let product_image = $(".product-image-" + index).val();

  console.log("quantity:", quantity);
  console.log("title:", product_title);
  console.log("id:", product_id);
  console.log("pid:", product_pid);
  console.log("image:", product_image);
  console.log("price:", product_price);
  console.log("Current element:", this_val);

  $.ajax({
      url: '/add_to_cart',
      data: {
          'id': product_id,
          'pid': product_pid,
          'image': product_image,
          'qty': quantity,
          'title': product_title,
          'price': product_price,
      },
      dataType: 'json',
      beforeSend: function () {
          console.log("adding product to cart...");
      },
      success: function (response) {
          console.log(response);
          if (response.already_in_cart) {
              this_val.html("Already");
          } else {
              this_val.html("Added ✔");
          }
          console.log("Added Product to Cart");
          $(".cart-items-count").text(response.totalcartitems);
      }
  });
});










$(".button-add-to-cart").on("click", function () {
  let button = $(this);
  let productContainer = button.closest('tr');
  let index = button.attr("data-index");

  let quantity = productContainer.find(".product-quantity-" + index).val();
  let product_title = productContainer.find(".product-title-" + index).val();
  let product_id = productContainer.find(".product-id-" + index).val();
  let product_price = parseFloat(productContainer.find(".current-product-price-" + index).text());
  let product_pid = productContainer.find(".product-pid-" + index).val();
  let product_image = productContainer.find(".product-image-" + index).val();

  console.log("Quantity:", quantity);
  console.log("Title:", product_title);
  console.log("ID:", product_id);
  console.log("PID:", product_pid);
  console.log("Image:", product_image);
  console.log("Price:", product_price);
  console.log("Current Element:", button);

  $.ajax({
      url: '/add_to_cart',
      data: {
          'id': product_id,
          'pid': product_pid,
          'image': product_image,
          'qty': quantity,
          'title': product_title,
          'price': product_price,
      },
      dataType: 'json',
      beforeSend: function () {
          console.log("Adding product to cart...");
      },
      success: function (response) {
          console.log(response);
          if (response.already_in_cart) {
              button.html("Already");
          } else {
              button.html("Added ✔");
          }
          console.log("Added Product to Cart");
          $(".cart-items-count").text(response.totalcartitems);
      }
  });
});




// modified 

// $(".button-add-to-cart").on("click", function () {
//   let button = $(this);
//   let productContainer = button.closest('tr');
//   let index = button.attr("data-index");

//   let quantityInput = $('<input type="hidden" value="1" name="product-quantity" class="w-25 mb-10 product-quantity-' + index + '">');
//   let productPidInput = $('<input type="text" class="product-pid-' + index + '" value="' + index + '">');
//   let productImageInput = $('<input type="hidden" class="product-image-' + index + '" value="image_url_here">');
//   let productIdInput = $('<input type="text" class="product-id-' + index + '" value="' + index + '">');
//   let productTitleInput = $('<input type="hidden" class="product-title-' + index + '" value="product_title_here">');

//   productContainer.append(quantityInput);
//   productContainer.append(productPidInput);
//   productContainer.append(productImageInput);
//   productContainer.append(productIdInput);
//   productContainer.append(productTitleInput);

//   let quantity = productContainer.find(".product-quantity-" + index).val();
//   let product_title = productContainer.find(".product-title-" + index).val();
//   let product_id = productContainer.find(".product-id-" + index).val();
//   let product_price = parseFloat(productContainer.find(".current-product-price-" + index).text());
//   let product_pid = productContainer.find(".product-pid-" + index).val();
//   let product_image = productContainer.find(".product-image-" + index).val();

//   console.log("Quantity:", quantity);
//   console.log("Title:", product_title);
//   console.log("ID:", product_id);
//   console.log("PID:", product_pid);
//   console.log("Image:", product_image);
//   console.log("Price:", product_price);
//   console.log("Current Element:", button);

//   $.ajax({
//       url: '/add_to_cart',
//       data: {
//           'id': product_id,
//           'pid': product_pid,
//           'image': product_image,
//           'qty': quantity,
//           'title': product_title,
//           'price': product_price,
//       },
//       dataType: 'json',
//       beforeSend: function () {
//           console.log("Adding product to cart...");
//       },
//       success: function (response) {
//           console.log(response);
//           if (response.already_in_cart) {
//               button.html("Already");
//           } else {
//               button.html("Added ✔");
//           }
//           console.log("Added Product to Cart");
//           $(".cart-items-count").text(response.totalcartitems);
//       }
//   });
// });





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



// $(document).on("click", ".add-to-wishlist", function(){
//   let product_id = $(this).attr("data-product-item")
//   let this_val = $(this)

//   console.log("PRODUCT ID IS", product_id)

//   $.ajax({
//     url: "add-to-wishlist/",
//     data: {
//       "id":product_id
//     },
//     dataType: "json",
//     beforeSend: function{
//       this_val.html("✓")
//     },
//     success: function{
//       console.log("Added to wishlist")
//     }
      
//   })
// })


$(document).on("click", ".add-to-wishlist", function(){
  let product_id = $(this).attr("data-product-item");
  let this_val = $(this);

  console.log("PRODUCT ID IS", product_id);

  $.ajax({
    url: "/add-to-wishlist",
    data: {
      "id": product_id
    },
    dataType: "json",
    beforeSend: function() {
      console.log("Adding to wishlist..")
    },
    success: function(response) {
      this_val.html("✓");
      if (response.bool === true){
        console.log("Added to wishlist");
      }
    }
  });
});



// Remove from wishlist
$(document).on("click", ".delete-wishlist-product", function(){
  let wishlist_id = $(this).attr("data-wishlist-product")
  let this_val = $(this)

  console.log("wishlist id is:", wishlist_id);

  $.ajax({
    url:"/remove-from-wishlist/",
    data:{
        "id": wishlist_id
   },
   dataType: "json",
   beforeSend: function(){
    console.log("Deleting product from wishlist...");
   },
   success: function(response){
    $("#wishlist-list").html(response.data)
    
   },
   
})
})


// Making default address

// $(document).on("click", ".make-default-address", function(){
//   let this_val = $(this);
//   let id = this_val.attr("data-address-id");  
  
//   console.log("ID is:", id);
//   console.log("Element is:", this_val);


//   $.ajax({
//       url:"/make-default-address",
//       data:{
//           "id":id
//       },
//       dataType:"json",
//       success: function(response){
//           console.log("Address made default...");
//           if (response.boolean == true){
//               $(".check").hide()
//               $(".action_btn").show()

//               $(".check"+id).show()
//               $(".button"+id).hide()
//           }
//       }

//   })
// });


$(document).on("click", ".make-default-address", function(){
  let this_val = $(this);
  let id = this_val.attr("data-address-id");  
  
  console.log("ID is:", id);
  console.log("Element is:", this_val);

  $.ajax({
    url: "/make-default-address/",
    data: {
      "id": id
    },
    dataType: "json",
    success: function(response){
      console.log("Address made default...");
      if (response.boolean == true){
        // Hide all checkmarks and show all buttons
        $(".fa-check-circle").hide();
        $(".make-default-address").show();

        // Show checkmark and hide button for the selected address
        $(".check" + id).show();
        $(".button" + id).hide();
      }
    }
  });
});






// category filter
$(document).ready(function (){
  $(".filter-checkbox ,#apply-filter-btn").on("click", function(){
    console.log("A checkbox have been clicked")  ;

    let filter_object = {}

    let min_price = $("#max_price").attr("min")
    let max_price = $("#max_price").val()

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    $(".filter-checkbox").each(function(){
      let filter_value = $(this).val()
      let filter_key = $(this).data("filter")
      // console.log("Filter value is:", filter_value);
      // console.log("Filter key is:", filter_key);

      filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
        return element.value
      })
    })
    console.log("Filter Object is: ",filter_object);
    $.ajax({
      url: '/filter-product',
      data: filter_object,
      dataType: 'json',
      beforeSend: function(){
        console.log("Trying to filter product...");
      },
      success: function(response){
        console.log(response);
        console.log("Data filtred successfully...")
        $("#filtered-product").html(response.data)
      }
    })
  })

  $("#max_price").on("blur",function(){
    let min_price = $(this).attr("min")
    let max_price = $(this).attr("max")
    let current_price = $(this).val()

    // console.log("Current Price is:", current_price);
    // console.log("Max Price is:", max_price);
    // console.log("Min Price is:", min_price);

    if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
      // console.log("Price error occures")

      min_Price = Math.round(min_price * 100) / 100 
      max_Price = Math.round(max_price * 100) / 100 

    
      // console.log("Min Price is:", min_Price);
      // console.log("Max Price is:", max_Price);

      alert("Price must be between $" + min_price + 'and $' + max_price)
      $(this).val(min_price)
      $('#range').val(min_price)
      
      $(this).focus()

      return false

    }
  })

})    
 



// function copyToClipboard(text) {
//   navigator.clipboard.writeText(text).then(() => {
//       Swal.fire({
//           position: 'center',
//           icon: 'success',
//           title: "Coupon Code copied to Clipboard",
//           showConfirmButton: false,
//           timer: 1500
//       });
//   }).catch(err => {
//       console.error('Unable to copy to clipboard', err);
//       // Handle error
//       Swal.fire({
//           position: 'center',
//           icon: 'error',
//           title: "Failed to copy Coupon Code",
//           showConfirmButton: false,
//           timer: 1500
//       });
//   });
// }





// function copyToClipboard(code) {
//   navigator.clipboard.writeText(code).then(()=> {
//       Swal.fire({
//       position: 'center',
//       icon: 'success',
//       title: "Coupon Code copied to Clipboard",
//       showConfirmButton: false,
//       timer: 1500
//       });
//   }).catch(err=>{
//       console.error('Unable to copy to clipboard', error);
//    });
//         }






// document.addEventListener('DOMContentLoaded', function () {
//   // Get all elements with the class 'copy-coupon-button'
//   var copyButtons = document.querySelectorAll('.copy-coupon-button');

//   // Loop through each button and attach a click event listener
//   copyButtons.forEach(function (button) {
//       button.addEventListener('click', function () {
//           // Find the sibling with the class 'coupon-code' to get the coupon code
//           var couponCodeElement = button.parentElement.querySelector('.coupon-code');

//           // Create a temporary input element
//           var tempInput = document.createElement('input');

//           // Set the value of the input to the coupon code
//           tempInput.value = couponCodeElement.innerText;

//           // Append the input to the body
//           document.body.appendChild(tempInput);

//           // Select the input's content
//           tempInput.select();

//           // Copy the selected content
//           document.execCommand('copy');

//           // Remove the temporary input element
//           document.body.removeChild(tempInput);

//           // Optionally, you can provide visual feedback to the user (e.g., show a tooltip)
//           // For example, using Bootstrap's tooltip:
//           var tooltip = new bootstrap.Tooltip(button, {
//               title: 'Copied!',
//               trigger: 'manual',
//               placement: 'top'
//           });

//           // Show the tooltip
//           tooltip.show();

//           // Hide the tooltip after a brief delay
//           setTimeout(function () {
//               tooltip.hide();
//           }, 1000);
//       });
//   });
// });





function copyCouponCode(code) {
  // Create a temporary textarea element
  const textarea = document.createElement('textarea');
  textarea.value = code; // Set the value to the coupon code
  document.body.appendChild(textarea); // Append the textarea to the DOM

  // Select and copy the code
  textarea.select();
  document.execCommand('copy');

  // Remove the textarea from the DOM
  document.body.removeChild(textarea);

  // Show a success message or perform any other action
  alert('Coupon code copied to clipboard: ' + code);
}





