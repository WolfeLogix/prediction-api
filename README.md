# prediction-api

## TODO List

- [ ] Data Structures
- [ ] Container to load the data to the database
- [ ] Queries to prepare the data into one table
- [ ] Run the Dataset through the POC juypter notebook
- [ ] (optional) build out the pytorch training in the api
  - [ ] Copy all the code from the juypter notebook
  - [ ] select the data
  - [ ] test/train split
  - [ ] instantiate the model
  - [ ] train the model
  - [ ] save the model to disk
- [ ] build out serving the model in the api
  - [ ] load in model
  - [ ] collect live data
  - [ ] transform the live data
  - [ ] make the prediction
  - [ ] reverse transform the prediction
  - [ ] return the prediction
- [ ] Build out the Trade Decision endpoint
  - [ ] Collect Data
  - [ ] Make the prediction
  - [ ] Make the trade decision
  - [ ] place trades with stop loss and take profit
  - [ ] write the trade to the database
  - [ ] return the trade to the user
- [ ] Orchistration in GH Actions
- [ ] CI/CD in GH Actions
- [ ] Deploy
