// https://docs.djangoproject.com/en/2.0/ref/csrf/#setting-the-token-on-the-ajax-request
const csrftoken = document.cookie.match(/csrftoken=(\w+);/)[1];
function csrfSafeMethod (method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (csrftoken && !csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  }
});

$('.product').each(function (idx, el) {
  const $product = $(el)
  console.log($product.data('id'))
  $product.on('click', '.product--ui-wishlist', function (e, el) {
    e.preventDefault()
    const $el = $(el)
  })
});
