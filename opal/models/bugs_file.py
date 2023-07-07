"""Contains the bugs file of models we want to implement with pyjags"""

POIS_GAMMA_MODEL = '''
model {
  # LIKELIHOOD AND RANDOM EFFECT MODEL FOR THE SCORING PROPENSITY
  for (g in 1:ngames) {
    # Observed number of goals scored by each team
    y1[g] ~ dpois(theta[g,1])
    y2[g] ~ dpois(theta[g,2])
    # Predictive distribution for the number of goals scored
    ynew[g,1] ~ dpois(theta[g,1])
    ynew[g,2] ~ dpois(theta[g,2])
    # Average Scoring intensities (accounting for mixing components)
    log(theta[g,1]) <- home_p + att[hometeam[g]] + def[awayteam[g]]
    log(theta[g,2]) <- att[awayteam[g]] + def[hometeam[g]]
  }
  
  # prior on the home effect
  home ~ dnorm(0,0.1)
  home_p <- 0 + home
  # Trick to code the sum-to-zero constraint
  for (t in 1:nteams){
    att.star[t] ~ dnorm(mu.att,tau.att)
    def.star[t] ~ dnorm(mu.def,tau.def)
    att[t] <- att.star[t] - mean(att.star[])
    def[t] <- def.star[t] - mean(def.star[])
  }
  # priors on the random effects
  mu.att ~ dnorm(0,0.1)
  mu.def ~ dnorm(0,0.1)
  tau.att ~ dgamma(.01,.01)
  tau.def ~ dgamma(.01,.01)
  
}
'''