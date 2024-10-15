const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
const noResults = document.querySelector(".no-results");
tableOutput.style.display = "none";
searchField.addEventListener("keyup", (e) => {
	const searchValue = e.target.value;

	if (searchValue.trim().length > 0) {
		paginationContainer.style.display = "none";
		tbody.innerHTML = "";
		fetch("/search-expenses", {
			body: JSON.stringify({ searchText: searchValue }),
			method: "POST",
		})
			.then((res) => res.json())
			.then((data) => {
				console.log("data", data);
				appTable.style.display = "none";
				tableOutput.style.display = "block";

				console.log("data.length", data.length);

				if (data.length === 0) {
					noResults.style.display = "block";
					tableOutput.style.display = "none";
				} else {
					noResults.style.display = "none";
					data.forEach((item) => {
						tbody.innerHTML += `					
						<tr>
						<td>${item.amount}</td>
						<td>${item.category}</td>
						<td>${item.description}</td>
						<td>${item.date}</td>
						<td><a href="{% url 'expense-edit' expense.id %}" class="btn btn-secondary btn-sm">Edit</a></td>
						</tr>`;
					});
				}
			});
	} else {
		paginationContainer.style.display = "block";
		appTable.style.display = "block";
		tableOutput.style.display = "none";

	}
});