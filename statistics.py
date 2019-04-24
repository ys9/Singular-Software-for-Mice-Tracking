class statistics:
    import numpy as np
    from scipy import stats

    def mean(data):
        sum = 0
        n = 0
        for x in data:
            n += 1
            sum += x
        return sum/n

    def sigma(data):
        m = mean(data)
        sum = 0
        n = 0
        for x in data:
            sum += (x - m)**2
            n += 1
        return sum/n

    def sd(data):
        return np.sqrt(sigma(data))

    # Calculates the pooled variance of two samples
    #
    # Use when it can be assumed that the two samples
    # have no significant difference in variance
    def pool_sigma(d1, d2):
        m1 = mean(d1)
        m2 = mean(d2)
        n1 = 0
        n2 = 0
        sum1 = 0
        sum2 = 0
        for x in d1:
            sum1 += (x-m1)**2
            n1 += 1
        for y in d2:
            sum2 += (y-m2)**2
            n2 += 1
        return (sum1 + sum2)/(n1 + n2 - 2)

    # Returns t statistic: float or array
    # Returns p value: two-tailed, float or array
    def one_sample_t(data, popmean):
        return scipy.stats.ttest_1samp(data, popmean)

    # Returns t stat and p value as float or array
    def two_samp_ind_t(d1, d2):
        return scipy.stats.ttest_ind(d1, d2)

    # Mann Whitney U Test
    # param d1: First data set
    # param d2: Second data set
    # param side: should be 'less,' 'greater,' or 'two-sided'
    # returns U statistic and p value
    def mann_whitney(d1, d2, side):
        return scipy.stats.mannwhitneyu(d1, d2, side='two-sided')

    # Corrects alpha value when using multiple tests
    # Simply divides alpha by number of tests done
    def bonferroni_alpha(alpha=0.05, p_vals):
        n = len(p_vals)
        return alpha / n

    # Determines which tests were stastitically significant given an alpha
    # param p_vals: array of p_values for a list of test p values
    # param alpha: alpha to determine significance. Default is 5%
    # return boolean array denoting significance (true=significant)
    def significance(p_vals, alpha = 0.05):
        sigs = [False] * len(p_vals)
        i = 0
        for x in p_vals:
            if x <= alpha:
                sigs[i] = True
        return sigs
