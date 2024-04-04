document.addEventListener("DOMContentLoaded", function() {
    const profileDropdown = document.getElementById('profileDropdown');
    const profileDropdownMenu = document.getElementById('profileDropdownMenu');

    profileDropdown.addEventListener('click', function(event) {
        profileDropdownMenu.classList.toggle('dropdown-menu');
    });

    document.addEventListener('click', function(event) {
        if (!profileDropdown.contains(event.target) && !profileDropdownMenu.contains(event.target)) {
            profileDropdownMenu.classList.add('dropdown-menu');
        }
    });
});
