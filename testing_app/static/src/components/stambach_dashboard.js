/** @odoo-module */


import {registry} from "@web/core/registry"
import {KpiCard} from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"

const { Component, onWillStart, useRef, onMounted , useState } = owl;

export class OwlStambachDashboard extends Component {

    setup() {
        this.state = useState({
            services: {
                value: 0,

            },
            patients: {
                value: 0,
            },
             tests: {
                value: 0,
            },
            period: 90,
        });

        this.orm = useService("orm");
        this.actionService = useService("action");

        onWillStart(async () => {
            await this.getServices();
            await this.getPatients();
            await this.getTests();
            await this.getMonthlyTests();


        });
    }



    async onChangePeriod(event) {
        const selectedPeriod = parseInt(event.target.value);
        this.state.period = selectedPeriod || 0;
        await this.getServices();
        await this.getPatients();
        await this.getTests();
        await this.getMonthlyTests();
    }



    async getServices() {
    const currentDate = new Date();
    const pastDate = new Date(currentDate);
    pastDate.setDate(pastDate.getDate() - this.state.period);

    const totalServices = await this.orm.searchCount("data.test", []);

    const servicesData = await this.orm.searchRead("data.test", [], ["name", "creation_date"]);

    const serviceCounts = {};
    servicesData.forEach(service => {
        const creationDate = new Date(service.creation_date);
        if (creationDate >= pastDate) {
            serviceCounts[service.name] = (serviceCounts[service.name] || 0) + 1;
        }
    });

    this.state.services.value = Object.keys(serviceCounts).length;
    this.state.services.data = Object.entries(serviceCounts).map(([name, count]) => ({
        name,
        count,

    }));


    if (totalServices > 0) {
        const percentage = (this.state.services.value / totalServices) * 100;
        this.state.services.percentage = percentage.toFixed(2);
    } else {
        this.state.services.percentage = 0;
    }
}

async getPatients() {
    const currentDate = new Date();
    const pastDate = new Date(currentDate);
    pastDate.setDate(pastDate.getDate() - this.state.period);

    const totalPatients = await this.orm.searchCount("res.partner", []);

    const patientsData = await this.orm.searchRead("res.partner", [['state_patient', '=', true]], ["name", "date_today"]);

    const patientCounts = {};
    patientsData.forEach(patient => {
        const patientDate = new Date(patient.date_today);
        if (patientDate >= pastDate) {
            patientCounts[patient.name] = (patientCounts[patient.name] || 0) + 1;
        }
    });

    this.state.patients.value = Object.keys(patientCounts).length;
    this.state.patients.data = Object.entries(patientCounts).map(([name, count]) => ({
        name,
        count,
    }));


    if (totalPatients > 0) {
        const percentage = (this.state.patients.value / totalPatients) * 100;
        this.state.patients.percentage = percentage.toFixed(2);
    } else {
        this.state.patients.percentage = 0;
    }
}

async getTests() {
    const currentDate = new Date();
    const pastDate = new Date(currentDate);
    pastDate.setDate(pastDate.getDate() - this.state.period);

    const totalTests = await this.orm.searchCount("stambach.test", []);

    const testsData = await this.orm.searchRead("stambach.test", [['date_today', '>=', pastDate.toISOString()]], ["date_today"]);

    this.state.tests.value = testsData.length;


    if (totalTests > 0) {
        const percentage = (this.state.tests.value / totalTests) * 100;
        this.state.tests.percentage = percentage.toFixed(2);
    } else {
        this.state.tests.percentage = 0;
    }
}

async getMonthlyTests() {
    const currentDate = new Date();
    const pastDate = new Date(currentDate);
    pastDate.setDate(pastDate.getDate() - this.state.period);

    const testsData = await this.orm.searchRead("stambach.test", [['date_today', '>=', pastDate.toISOString()]], ["date_today"]);

    const monthlyTests = {};
    testsData.forEach(test => {
        const testDate = new Date(test.date_today);
        const month = testDate.getMonth() + 1;
        monthlyTests[month] = (monthlyTests[month] || 0) + 1;
    });

    this.state.tests.monthlyData = Object.entries(monthlyTests).map(([month, count]) => ({
        month,
        count,

    }));
}


   async handleServiceClick() {
    await this.openModelView("data.test", "Services");
}

async handlePatientClick() {
    await this.openModelView("res.partner", "Patients", [['state_patient', '=', true]]);
}

async handleTestClick() {
    await this.openModelView("stambach.test", "Tests");
}

async openModelView(model, name, domain = []) {
    await this.actionService.doAction({
        type: "ir.actions.act_window",
        name: name,
        res_model: model,
        views: [[false, "list"]],
        domain: domain,
    });
}


}


OwlStambachDashboard.template = "owl.OwlStambachDashboard";
OwlStambachDashboard.components={ KpiCard , ChartRenderer };

registry.category("actions").add("owl.stambach_test_dashboard", OwlStambachDashboard);
