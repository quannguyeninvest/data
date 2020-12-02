import numpy as np
import pandas as pd
import alphalens as al
import matplotlib.pyplot as plt
import seaborn as sns

@al.plotting.customize
def create_returns_tear_sheet(factor_data, by_group=False):
    """ Simple create returns tear sheet for factor analysis
    """
    mean_quant_ret, std_quantile = al.performance.mean_return_by_quantile(
        factor_data, demeaned=False
    )
    mean_quant_rateret = mean_quant_ret.apply(
        al.utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0]
    )
    std_quantile_rate = std_quantile.apply(
        al.utils.std_conversion, axis=0, base_period=std_quantile.columns[0]
    )

    mean_quant_ret_bydate, std_quant_daily = al.performance.mean_return_by_quantile(
        factor_data, by_date=True, demeaned=False
    )
    mean_quant_rateret_bydate = mean_quant_ret_bydate.apply(
        al.utils.rate_of_return, axis=0, base_period=mean_quant_ret_bydate.columns[0],
    )

    gf = al.tears.GridFigure(rows=2, cols=1)
    al.plotting.plot_quantile_returns_bar(
        mean_quant_rateret.join(std_quantile_rate.add_suffix('_err')),
        by_group=False,
        ylim_percentiles=None,
        ax=gf.next_row()
    )
    al.plotting.plot_quantile_returns_violin(
        mean_quant_rateret_bydate, ylim_percentiles=(1, 99), ax=gf.next_row()
    )
    plt.show()
    gf.close()
    
    if by_group:
        (
            mean_return_quantile_group,
            mean_return_quantile_group_std_err,
        ) = al.performance.mean_return_by_quantile(
            factor_data,
            by_group=True,
            demeaned=False
        )

        mean_quant_rateret_group = mean_return_quantile_group.apply(
            al.utils.rate_of_return,
            axis=0,
            base_period=mean_return_quantile_group.columns[0],
        )
        quantile_group_ratestd_err = mean_return_quantile_group_std_err.apply(
            al.utils.std_conversion,
            axis=0,
            base_period=mean_return_quantile_group_std_err.columns[0],
        )

        num_groups = len(
            mean_quant_rateret_group.index.get_level_values("group").unique()
        )

        vertical_sections = 1 + (((num_groups - 1) // 2) + 1)
        gf = al.tears.GridFigure(rows=vertical_sections, cols=2)

        ax_quantile_returns_bar_by_group = [
            gf.next_cell() for _ in range(num_groups)
        ]
        al.plotting.plot_quantile_returns_bar(
            mean_quant_rateret_group.join(quantile_group_ratestd_err.add_suffix('_err')),
            by_group=True,
            ylim_percentiles=(1, 99),
            ax=ax_quantile_returns_bar_by_group,
        )
        plt.show()
        gf.close()


@al.plotting.customize
def create_ir_heatmap(factor_data, y_column, key=None):
    rets = al.utils.get_forward_returns_columns(factor_data.columns)[0]
    grpd = factor_data.groupby(['factor_quantile', y_column])[[rets]]

    irs = (grpd.mean() / grpd.std()).reset_index()

    return sns.heatmap(
        irs.pivot(index=y_column, columns='factor_quantile', values=rets).sort_index(ascending=False, key=key),
        cmap=sns.diverging_palette(0, 240, s=100, l=55, center="dark", as_cmap=True))
