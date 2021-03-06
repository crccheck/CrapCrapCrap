// https://docs.djangoproject.com/en/2.0/ref/csrf/#setting-the-token-on-the-ajax-request
const csrftoken = document.cookie.match(/csrftoken=(\w+);?/)[1]
function csrfSafeMethod (method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (csrftoken && !csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken)
    }
  },
})

$.ajax('/api/list/', {
  success: (data) => {
    data.wishlist.forEach((id) => {
      $(`.ProductSlat[data-id=${id}] .ProductSlat--ui-wishlist`)
        .addClass('active')
    })
  },
})

$('.ProductSlat').each(function (idx, el) {
  const $product = $(el)
  $product.on('click', '.ProductSlat--ui-wishlist', function (e, el) {
    e.preventDefault()
    const $el = $(this)
    const method = $el.hasClass('active') ? 'DELETE' : 'PUT'
    $.ajax($el.attr('href'), {
      method,
      contentType: 'application/json',
      data: JSON.stringify({
        products: [$product.data('id')],
      }),
      success: (data) => {
        Object.keys(data).forEach((id) => {
          $(`.ProductSlat[data-id=${id}] .ProductSlat--ui-wishlist`)
            .toggleClass('active', method === 'PUT')
        })
      },
    })
  })
})
