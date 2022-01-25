'use strict';

document.addEventListener('DOMContentLoaded', function () {
// ------------------------------------------------------- //
// Sidebar Functionality
// ------------------------------------------------------ //
    const sbToggleBtn = document.getElementById('toggle-btn'),
          sideNavbar  = document.querySelector('.side-navbar'),
          innerContent = document.querySelector('.content-inner'),
          smBrand = document.querySelector('.navbar-header .brand-small'),
          lgBrand = document.querySelector('.navbar-header .brand-big');

    if (sideNavbar) {
        sbToggleBtn.addEventListener('click', function (e) {
            e.preventDefault();
            this.classList.toggle('active');

            sideNavbar.classList.toggle('shrinked');
            innerContent.classList.toggle('active');
            document.dispatchEvent(new Event('sidebarChanged'));
          
        });
    }

// ------------------------------------------------------- //
// Footer
// ------------------------------------------------------ //
    let footer = document.querySelector('#footer');
    if (footer) {
        document.addEventListener('sidebarChanged', function () {
            adjustFooter();
        });
        window.addEventListener('resize', function () {
            adjustFooter();
        });
    }

    function adjustFooter() {
        var footerBlockHeight = document.querySelector('#footer').outerHeight;
        innerContent.style.paddingBottom = `${footerBlockHeight}px`;
    }
});