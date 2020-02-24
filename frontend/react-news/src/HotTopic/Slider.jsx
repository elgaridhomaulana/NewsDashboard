import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

const useStyles = makeStyles(theme => ({
	root: {
		width: 400,
	},
	margin: {
		height: theme.spacing(3),
	},
}));

function valuetext(value) {
	return `${value}°C`;
}


const MySlider = (props) => {
	const classes = useStyles();
	return (
		<div className={classes.root}>
			<Slider
				valueLabelDisplay="auto"
				color='secondary'
				value={props.value} onChange={(e, val) => props.onSlide(val)}
				aria-labelledby="continuous-slider"
				min={1}
				max={10} />
		</div>

	)
}

export default MySlider;