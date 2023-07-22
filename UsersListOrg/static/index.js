

const vm = new Vue({
    el: '#vm',
    delimiters: ['[[', ']]'],
    data: {
    orgStaffValue: false,
    selectedOption: '',
    selectedOptionChapter: '',
    isVisible: false,
    showConfirmation: false,
    },
  methods: {
    toggleElement() {
      this.isVisible = !this.isVisible;
      this.showConfirmation = false;
    },
    showDeleteModal() {
      this.showConfirmation = true;
    },
    cancelDelete() {
      this.showConfirmation = false;
      this.isVisible = false;
     },
  }
})

    const updBtn = document.getElementById("updBtn");
    let clickedId = ''
    if(updBtn) updBtn.addEventListener("click", function (event) {
            const delBtns = document.querySelectorAll(".del-btn");
            console.log(delBtns)
        delBtns.forEach((button) => {
        console.log("Button ID:", button.id); // Check the button IDs
        button.addEventListener("click", function (event) {
          clickedId = event.target.id;
          console.log("Clicked ID:", clickedId);

           const delBtnsYes = document.querySelectorAll(".del-btn-yes");
            delBtnsYes.forEach((div) => {
             const divId = div.id
             if (divId != clickedId) {
             div.classList.add("hide");
             }
          });

        });

      });

    });






   // to synchronize the form checkbox org_staff state with the Vue instance
      document.addEventListener("DOMContentLoaded", function () {
        const orgStaffCheckbox = document.getElementById("orgStaffCheckbox");
        if (orgStaffCheckbox?.checked) vm.orgStaffValue = orgStaffCheckbox.checked;
        orgStaffCheckbox?.addEventListener("change", function () {
          vm.orgStaffValue = orgStaffCheckbox.checked;
        });
      });