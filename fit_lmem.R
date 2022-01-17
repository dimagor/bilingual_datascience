library(lme4)
library(lmerTest)


compute_estimates_and_conf_ints <- function(data, formula, ci_method='profile'){
    model <- lmer(
        formula,
        data=data
    )

    # get model coefficients
    coeffs <- coef(
        summary(model)
    )

    # compute confidence intervals
    cis <- confint(
        model,
        method=ci_method
    )

    intercept_estimate <- coeffs[c('(Intercept)'), ][c('Estimate', 'Pr(>|t|)')]
    intercept_ci <- cis[c('(Intercept)'), ]

    time_estimate <- coeffs[c('Time'), ][c('Estimate', 'Pr(>|t|)')]
    time_ci <- cis[c('Time'), ]

    return(list(
        'estimate_intercept'=intercept_estimate,
        'estimate_time'=time_estimate,
        'conf_int_intercept'=intercept_ci,
        'conf_int_time'=time_ci
    ))
}
