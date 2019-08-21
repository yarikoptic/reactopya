import React, { Component } from 'react';
import * as allWidgets from '../../{{ project_name }}_widgets';
import { Paper, Grid, IconButton } from "@material-ui/core";
import { FaExpandArrowsAlt, FaCompressArrowsAlt } from "react-icons/fa";

class LazyLoader extends Component {
    constructor(props) {
        super(props);
        this.state = {
            hasBeenVisible: false
        };
        this.unmounted = false;
    }

    async componentDidMount() {
        this.startChecking();
    }

    componentWillUnmount() {
        this.unmounted = true;
    }

    componentDidUpdate(prevProps, prevState) {
    }

    startChecking() {
        this.doCheck();
        if (this.state.hasBeenVisible) return;
        if (this.unmounted) return;
        setTimeout(() => {
            this.startChecking();
        }, 1000);
    }

    doCheck() {
        if (this.state.hasBeenVisible) return;
        if (this.isInViewport(this.container)) {
            this.setState({ hasBeenVisible: true });
        }
    }

    isInViewport(elem) {
        if (!elem) return false;
        var bounding = elem.getBoundingClientRect();
        return (
            bounding.top >= 0 &&
            bounding.left >= 0 &&
            bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };

    render() {
        if (!this.state.hasBeenVisible) {
            return (
                <div className="lazyloader" ref={el => (this.container = el)}></div>
            )
        }
        else {
            return this.props.children;
        }
    }
}

export default class MainWindow extends Component {
    state = {
        expandedWidget: null
    };
    handleToggleExpand = (widget) => {
        if (this.state.expandedWidget) {
            this.setState({
                expandedWidget: null
            });
        }
        else {
            this.setState({
                expandedWidget: widget
            });
        }
    }
    render() {
        const { config } = this.props;
        const { expandedWidget } = this.state;
        const style0 = { overflowX: 'hidden', margin: 10, padding: 20, background: 'lightblue' };
        const style1 = { padding: 20, margin: 10, minHeight: 800 };
        let widgets = [];
        if (expandedWidget) {
            widgets.push(expandedWidget);
        }
        else {
            let gallery_widgets = config.gallery_widgets;
            if (!gallery_widgets) {
                gallery_widgets = [];
                for (let key in allWidgets) {
                    gallery_widgets.push({
                        name: key
                    });
                }
            }
            for (let a of config.gallery_widgets) {
                let component = allWidgets[a.name];
                widgets.push({
                    component: component,
                    title: a.title || component.title || a.name,
                    props: a.props || (component.reactopyaConfig || {}).galleryProps || {}
                });
            }
        }
        let item_sizes = {
            xs: 12,
            md: 6,
            xl: 4
        };
        let expandOrCollapseIcon = null;
        if (expandedWidget) {
            item_sizes.xs = item_sizes.md = item_sizes.xl = 12;
            expandOrCollapseIcon = <FaCompressArrowsAlt />
        }
        else {
            expandOrCollapseIcon = <FaExpandArrowsAlt />
        }
        return (
            <div style={style0}>
                <Grid container style={style0}>
                    {
                        widgets.map((widget) => {
                            let Comp = widget.component;
                            return <Grid key={widget.title} item {...item_sizes}>
                                <Paper style={style1}>
                                    <Grid container alignItems={'flex-start'} justify={'flex-end'} direction={'row'}>
                                        <IconButton
                                            onClick={() => { this.handleToggleExpand(widget) }}
                                            size={'small'}
                                        >
                                            {expandOrCollapseIcon}
                                        </IconButton>
                                    </Grid>

                                    <hr />
                                    <h2>{widget.title}</h2>
                                    <hr />
                                    <LazyLoader>
                                        <Comp {...(widget.props)} />
                                    </LazyLoader>
                                </Paper>
                            </Grid>;
                        })
                    }
                </Grid>
            </div>
        );
    }
}
