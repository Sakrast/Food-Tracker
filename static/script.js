const foodForm = document.querySelector('.food-container');
const overlay = document.querySelector('.overlay');
const btnCloseForm = document.querySelector('.close-container');
const btnOpenForm = document.querySelector('.open-form');

const openForm = function (e) {
  e.preventDefault();
  foodForm.classList.remove('hidden');
  overlay.classList.remove('hidden');
};

const closeForm = function () {
  foodForm.classList.add('hidden');
  overlay.classList.add('hidden');
};

btnOpenForm.addEventListener('click', openForm)

btnCloseForm.addEventListener('click', closeForm);
overlay.addEventListener('click', closeForm);

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape' && !foodForm.classList.contains('hidden')) {
    closeForm();
  }
});