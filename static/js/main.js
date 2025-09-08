// Main JavaScript file for FBC Library System

// Document Ready
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Handle notification marking as read
    $('.notification-dropdown .unread').click(function(e) {
        const notificationId = $(this).data('notification-id');
        $.post('/notifications/mark-as-read/', { id: notificationId })
            .done(function(response) {
                // Update UI if needed
            });
    });

    // Book search functionality
    $('#book-search-form').on('submit', function(e) {
        e.preventDefault();
        const searchQuery = $('#search-input').val();
        const searchCategory = $('#search-category').val();
        
        showSpinner();
        
        $.get('/books/search/', { q: searchQuery, category: searchCategory })
            .done(function(response) {
                $('#book-grid').html(response.html);
            })
            .fail(function(error) {
                showAlert('Error searching books. Please try again.', 'danger');
            })
            .always(function() {
                hideSpinner();
            });
    });

    // Payment method selection
    $('.payment-option').click(function() {
        $('.payment-option').removeClass('selected');
        $(this).addClass('selected');
        $('#selected-payment-method').val($(this).data('method'));
    });

    // Handle book borrowing
    $('.borrow-book-btn').click(function(e) {
        e.preventDefault();
        const bookId = $(this).data('book-id');
        
        showSpinner();
        
        $.post('/books/borrow/', { book_id: bookId })
            .done(function(response) {
                if (response.success) {
                    showAlert('Book borrowed successfully!', 'success');
                    updateBookAvailability(bookId, response.available_copies);
                } else {
                    showAlert(response.message, 'warning');
                }
            })
            .fail(function(error) {
                showAlert('Error borrowing book. Please try again.', 'danger');
            })
            .always(function() {
                hideSpinner();
            });
    });

    // E-book reader page tracking
    if ($('#ebook-reader').length) {
        let lastPage = localStorage.getItem('ebook-page-' + $('#ebook-reader').data('book-id'));
        if (lastPage) {
            $('#ebook-reader').turn('page', parseInt(lastPage));
        }

        $('#ebook-reader').on('turned', function(e, page) {
            localStorage.setItem('ebook-page-' + $(this).data('book-id'), page);
        });
    }
});

// Utility Functions

function showSpinner() {
    if (!$('.spinner-overlay').length) {
        $('body').append(`
            <div class="spinner-overlay">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `);
    }
}

function hideSpinner() {
    $('.spinner-overlay').remove();
}

function showAlert(message, type = 'info') {
    const alert = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const alertContainer = $('.alert-container');
    if (alertContainer.length) {
        alertContainer.append(alert);
    } else {
        $('.container').first().prepend(`<div class="alert-container">${alert}</div>`);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
}

function updateBookAvailability(bookId, availableCopies) {
    const bookCard = $(`[data-book-id="${bookId}"]`);
    bookCard.find('.available-copies').text(availableCopies);
    
    if (availableCopies === 0) {
        bookCard.find('.borrow-book-btn')
            .prop('disabled', true)
            .text('Not Available');
    }
}

// Payment Processing Functions

function initializePaymentForm(paymentMethod) {
    switch(paymentMethod) {
        case 'stripe':
            initializeStripeForm();
            break;
        case 'paypal':
            initializePayPalButtons();
            break;
        case 'orange_money':
        case 'afrimoney':
        case 'qmoney':
            initializeMobileMoneyForm();
            break;
    }
}

function initializeStripeForm() {
    // Stripe integration code will go here
    console.log('Initializing Stripe form...');
}

function initializePayPalButtons() {
    // PayPal integration code will go here
    console.log('Initializing PayPal buttons...');
}

function initializeMobileMoneyForm() {
    // Mobile money integration code will go here
    console.log('Initializing mobile money form...');
}

// File Upload Preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            $('#image-preview').attr('src', e.target.result).show();
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Export functions for use in other scripts
window.FBCLibrary = {
    showSpinner,
    hideSpinner,
    showAlert,
    updateBookAvailability,
    initializePaymentForm
};
