// static/your_app/js/script.js


// Report menu icon 
// Report menu icon 

const reportIcons = document.querySelectorAll('.report-icon');
const reportPopups = document.querySelectorAll('.report-popup');

reportIcons.forEach((icon, index) => {
    const popup = reportPopups[index];

    icon.addEventListener('click', (e) => {
        e.stopPropagation(); // جلوی بسته شدن سریع رو میگیره

        // اول همه‌ی popup ها رو ببند
        reportPopups.forEach(p => p.style.display = 'none');

        // فقط همونی که کلیک شده باز شه
        popup.style.display = 'block';
    });
});

// بستن همه popup ها وقتی بیرون کلیک شد
document.addEventListener('click', () => {
    reportPopups.forEach(p => p.style.display = 'none');
});


// Navbar JS code 

const menuLogo = document.querySelector('.menu-logo');
const menuProfile = document.querySelector('.profile-menu-pic');
const menuListMobile = document.querySelector('.menu-items');
const menuListDesktop = document.querySelector('.menu-items-desktop');

function toggleMobileMenu() {
    if (menuListMobile.style.display === "flex") {
        menuListMobile.style.display = "none";
    } else {
        menuListMobile.style.display = "flex";
    }
}

function toggleDesktopMenu() {
    menuListDesktop.classList.toggle('menu-popup');
}

menuLogo.addEventListener('click', toggleMobileMenu);
menuProfile.addEventListener('click', toggleDesktopMenu);



// opening comments section 
// opening comments section 

const commentSections = document.querySelectorAll('.post-comments-box');
const commentIcons = document.querySelectorAll('.comment-icon');

commentIcons.forEach((icon, index) => {
    icon.addEventListener('click', () => {
        const section = commentSections[index];
        if (section.style.display === 'block') {
            section.style.display = 'none';
        } else {
            section.style.display = 'block';
        }
    });
});


// liked post 
// liked post 

// document.querySelectorAll('.post-like').forEach(btn => {
//     btn.addEventListener('click', () => {
//         const icon = btn.querySelector('i');
//         const count = btn.querySelector('.post-like-num');
//         const liked = icon.classList.contains('liked');

//         if (liked) {
//             icon.classList.remove('liked');
//             icon.classList.remove('ri-heart-fill');
//             icon.classList.add('ri-heart-line');
//             count.textContent = parseInt(count.textContent) - 1;
//         } else {
//             icon.classList.add('liked');
//             icon.classList.remove('ri-heart-line');
//             icon.classList.add('ri-heart-fill');
//             count.textContent = parseInt(count.textContent) + 1;
//         }
//     });
// });



// this check contents on p tags that are in feed 
// this check contents on p tags that are in feed 

function adjustTextAlignment() {
    const posts = document.querySelectorAll(".post-text");

    posts.forEach(post => {
        const text = post.textContent.trim();

        if (/[\u0600-\u06FF]/.test(text)) {

            post.style.direction = "rtl";
            post.style.textAlign = "right";
        } else {

            post.style.direction = "ltr";
            post.style.textAlign = "left";
        }
    });
}


adjustTextAlignment();



// Ltr or Rtl checker for new post 
// Ltr or Rtl checker for new post 

document.getElementById("post-textarea").addEventListener("input", function () {
    const value = this.value.trim();

    if (/[\u0600-\u06FF]/.test(value)) {
        this.style.direction = "rtl";
        this.style.textAlign = "right";
    } else {
        this.style.direction = "ltr";
        this.style.textAlign = "left";
    }
});

document.querySelectorAll('.reply-toggle-btn').forEach((btn) => {
    btn.addEventListener('click', function () {
        const replyBox = this.closest('.comment').querySelector('.reply-box');
        replyBox.style.display = replyBox.style.display === 'none' ? 'block' : 'none';
    });
});


