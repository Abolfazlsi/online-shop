$(document).ready(function () {
    $('#comment_form').on('submit', function (e) {
        e.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'), // استفاده از ویژگی action فرم
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === 'success') {
                    let newCommentHTML = '<div class="d-flex">' +
                        '<div>' +
                        '<p class="mb-2" style="font-size: 14px;">' + response.created_at + '</p>' +
                        '<div class="d-flex justify-content-between">' +
                        '<h5>' + response.user_username + '</h5>' +
                        '</div>' +
                        '<p>' + response.comment_text + '</p>' +
                        '</div>' +
                        '</div>';
                    // افزودن کامنت جدید به بالای لیست کامنت‌ها
                    $('#nav-mission').prepend(newCommentHTML);
                    $('#comment_form textarea[name="text"]').val(''); // پاک کردن textarea
                } else {
                    alert('Error: ' + JSON.stringify(response.errors));
                }
            }
        });
    });
});

