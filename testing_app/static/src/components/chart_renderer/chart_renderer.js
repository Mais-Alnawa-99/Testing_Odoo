/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl




export class ChartRenderer extends Component {
    setup(){
        this.chartRef = useRef("chart");
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js");
        });

        onMounted(()=>this.renderChart());
    }

   renderChart() {
    if (this.props.type === 'doughnut') {
        const data = {
            labels: this.props.data.map(item => item.name),
            datasets: [{
                data: this.props.data.map(item => item.count),
                backgroundColor: this.props.colors || ['#FF6384', '#36A2EB', '#FFCE56'],
            }],
        };

        new Chart(this.chartRef.el, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: this.props.title,
                    },
                },
            },
        });
    } else if (this.props.type === 'pie') {
        const data = {
            labels: this.props.data.map(item => item.name),
            datasets: [{
                data: this.props.data.map(item => item.count),
                backgroundColor: this.props.colors || ['#FFCE56', '#4BC0C0', '#FF6384'],
            }],
        };

        new Chart(this.chartRef.el, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: this.props.title,
                    },
                },
            },
        });
    } else if (this.props.type === 'bar') {
        const data = {
            labels: this.props.data.map(item => `Month ${item.month}`),
            datasets: [{
                label: this.props.title,
                data: this.props.data.map(item => item.count),
                backgroundColor: this.props.colors || '#36A2EB',
            }],
        };

        new Chart(this.chartRef.el, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: this.props.title,
                    },
                },
            },
        });
    }
}


}

ChartRenderer.template = "owl.ChartRenderer";