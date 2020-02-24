/* global Plotly:true */
import React from 'react';
import createPlotlyComponent from 'react-plotly.js/factory';

class HotTopic extends React.Component {

	render() {
		const Plot = createPlotlyComponent(Plotly);
		const data = this.props.data
		let data_to_plot = []
		let panjang_array = Object.keys(this.props.data[0]).length - 1
		let topic = Object.keys(this.props.data[0]).splice(0, panjang_array)

		for (const key of topic) {
			data_to_plot.push({
				type: 'scatter',
				mode: 'lines+points',
				x: data.map(item => item.index),
				y: data.map(item => item[key]),
				name: key
			})
		}
		return (
			React.createElement(Plot, {
				data: data_to_plot,
				layout: {
					title: 'Hot Topic',
					margin: {
						l: 50,
						r: 50,
						b: 20,
						t: 30,
					}
				},
				style: { width: "100%", height: "100%" }
			})
		)
	}
}

export default HotTopic;