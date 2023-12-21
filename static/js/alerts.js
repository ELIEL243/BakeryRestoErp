"use strict";

(function (NioApp, $) {
  'use strict'; // Basic Sweet Alerts

$('.eg-swal-stock').on("click", function (e) {
    Swal.fire({
      position: 'top-end',
      icon: 'error',
      title: 'Stock insuffisant !',
      showConfirmButton: false,
      timer: 1500
    });
    e.preventDefault();
  });


})(NioApp, jQuery);