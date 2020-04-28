// 加载图表数据
var time=senti_data.time;
var senti_kinds=senti_data.senti_kinds;
var senti_prop=senti_data.senti_prop;
var num=senti_data.num;
var pos_num=senti_data.pos_num;
var neg_num=senti_data.neg_num;
var avg=senti_data.avg;
var pos_avg=senti_data.pos_avg;
var neg_avg=senti_data.neg_avg;
var senti_sum=senti_data.senti_sum;
var pos_sum=senti_data.pos_sum;
var neg_sum=senti_data.neg_sum;

$(function() {
        //初始化echarts
        var  ec1 = echarts.init(document.getElementById('num1'));
        var  ec2 = echarts.init(document.getElementById('num2'));
        var  ec3 = echarts.init(document.getElementById('num3'));
        var  ec4 = echarts.init(document.getElementById('num4'));

        var  ec5 = echarts.init(document.getElementById('sum1'));
        var  ec6 = echarts.init(document.getElementById('sum2'));
        var  ec7 = echarts.init(document.getElementById('sum3'));

        var  ec8 = echarts.init(document.getElementById('avg1'));
        var  ec9 = echarts.init(document.getElementById('avg2'));
        var  ec10 = echarts.init(document.getElementById('avg3'));


        loacl_senti_prop=[]
        for (i=0;i<senti_kinds.length;i++){
            loacl_senti_prop.push({
                "name": senti_kinds[i],
                "value": senti_prop[i],
            });
        }

        //配置option
        var option1 = {
            //标题内容
            title: {
	        text: '各类弹幕占比',
            left:'center'
	    },
            //定义鼠标提示框内容
            tooltip: {
                trigger: 'item',
                formatter: '{b} : {d}%'
            },
            //工具盒
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    //重新加载
                    restore: {},
                    //下载图片
                    saveAsImage: {},
                    dataView:{}
                },

    },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: senti_kinds
            },
            series: [{
                name:'各类弹幕占比',
                type: 'pie',
                radius: '65%',
                data: loacl_senti_prop,
            }
    ]
    };

        var option2={
            title: {
                text: '弹幕数量',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '弹幕数量',
                type: 'bar',
                data: num,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option3={
            title: {
                text: '正面弹幕数量',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '正面弹幕数量',
                type: 'bar',
                data: pos_num,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option4={
            title: {
                text: '负面弹幕数量',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '负面弹幕数量',
                type: 'bar',
                data: neg_num,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option5={
            title: {
                text: '弹幕片段情感值',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '弹幕片段情感值',
                type: 'bar',
                data: senti_sum,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option6={
            title: {
                text: '正面片段情感值',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '正面片段情感值',
                type: 'bar',
                data: pos_sum,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option7={
            title: {
                text: '负面弹片段情感值',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '负面弹片段情感值',
                type: 'bar',
                data: neg_sum,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option8={
            title: {
                text: '弹幕片段情感均值',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '弹幕片段情感均值',
                type: 'bar',
                data: avg,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option9={
            title: {
                text: '正面片段情感均值',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '正面片段情感均值',
                type: 'bar',
                data: pos_avg,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        var option10={
            title: {
                text: '负面弹片段情感均值',
                left:'center'
	        },
            tooltip: {
                show:true,
            },
            toolbox: {
                orient: 'vertical',
                show: true,
                feature: {
                    restore: {},
                    saveAsImage: {},
                    magicType:{
                        type: ['bar','line',]
                    },
                    dataView:{},
                },

            },
            xAxis: {
                type: 'category',
                data: time
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: '负面弹片段情感均值',
                type: 'bar',
                data: neg_avg,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
                },]
        };

        //设置option
        ec1.setOption(option1);
        ec2.setOption(option2);
        ec3.setOption(option3);
        ec4.setOption(option4);
        ec5.setOption(option5);
        ec6.setOption(option6);
        ec7.setOption(option7);
        ec8.setOption(option8);
        ec9.setOption(option9);
        ec10.setOption(option10);

    });