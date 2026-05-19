// 👉 Pour la page "Objectifs"
function initObjectifPage() {
  console.log("✅ Page Objectifs chargée.");
}

// 👉 Pour la page "Machines génératrices"
function ajouterMachinePersonnalisee() {
  const container = document.getElementById("machines_perso_container");
  const bloc = document.createElement("div");
  bloc.classList.add("machine-bloc");
  bloc.style.display = "grid";
  bloc.style.gridTemplateColumns = "1.5fr 1fr 1fr";
  bloc.style.gap = "15px";

  bloc.innerHTML = `
    <input type="text" name="machine_perso_nom[]" placeholder="Nom de la machine" required>
    <input type="number" name="machine_perso_nb[]" placeholder="Nombre" min="1" required>
    <input type="number" name="machine_perso_energie[]" placeholder="Wh/h" step="0.1" required>
  `;

  container.appendChild(bloc);
}

// 👉 Pour la page "Tarification"
function genererTranches(devise = "€") {
  const nb = parseInt(document.getElementById("nb_tranches").value);
  const container = document.getElementById("tranches_inputs");
  container.innerHTML = "";

  for (let i = 0; i < nb; i++) {
    const bloc = document.createElement("div");
    bloc.classList.add("grid-2col");

    bloc.innerHTML = `
      <div class="inline-field">
        <label>Tranche ${i + 1} (limite kWh) :</label>
        <input type="number" name="tranche_limite[]" step="1" required>
      </div>
      <div class="inline-field">
        <label>Tarif (${devise}/kWh) :</label>
        <input type="number" name="tranche_tarif[]" step="0.01" required>
      </div>
    `;

    container.appendChild(bloc);
  }
}

function afficherChampsTarification() {
  const type = document.getElementById("type_tarif").value;
  const devise = document.getElementById("devise")?.value || "€";
  const container = document.getElementById("champs_tarif");
  container.innerHTML = "";

  if (type === "forfait") {
    container.innerHTML = `
      <div class="inline-field">
        <label>Prix annuel (${devise}) :</label>
        <input type="number" name="prix_annuel" min="0" step="0.01" required>
      </div>
    `;
  } else if (type === "tranches") {
    container.innerHTML = `
      <div class="inline-field">
        <label>Nombre de tranches :</label>
        <input type="number" id="nb_tranches" min="1" required onchange="genererTranches('${devise}')">
      </div>
      <div id="tranches_inputs" style="margin-top: 15px;"></div>
    `;
  } else if (type === "heures") {
    container.innerHTML = `
      <div class="inline-field">
        <label>Tarif heures pleines (${devise}/kWh) :</label>
        <input type="number" name="tarif_hp" step="0.01" required>
      </div>
      <div class="inline-field">
        <label>Tarif heures creuses (${devise}/kWh) :</label>
        <input type="number" name="tarif_hc" step="0.01" required>
      </div>
    `;
  } else if (type === "abonnement") {
    container.innerHTML = `
      <div class="inline-field">
        <label>Prix abonnement annuel (${devise}) :</label>
        <input type="number" name="abonnement_annuel" step="0.01" required>
      </div>
      <div class="inline-field">
        <label>Tarif consommation (${devise}/kWh) :</label>
        <input type="number" name="tarif_conso" step="0.01" required>
      </div>
    `;
  }
}


// 👉 Init selon la page
document.addEventListener("DOMContentLoaded", () => {
  if (document.body.classList.contains("page-machines")) {
    const btn = document.getElementById("ajouter_machine_btn");
    if (btn) btn.addEventListener("click", ajouterMachinePersonnalisee);
  }

  if (document.body.classList.contains("page-objectif")) {
    initObjectifPage();
  }

  if (document.body.classList.contains("page-tarification")) {
    const selectTarif = document.getElementById("type_tarif");
    const selectDevise = document.getElementById("devise");
    if (selectTarif && selectDevise) {
      selectTarif.addEventListener("change", afficherChampsTarification);
      selectDevise.addEventListener("change", afficherChampsTarification);
      afficherChampsTarification(); // au chargement
    }
  }
});