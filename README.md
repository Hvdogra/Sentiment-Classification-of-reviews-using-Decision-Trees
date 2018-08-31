# Sentiment-Classification-of-reviews-using-Decision-Trees
It involves the use of decision trees to model the classification of reviews as positive and negative reviews. Then, feature bagging is applied to model random forests. Finally, we use pruning to improve the efficiency of the model.
# Assumptions
-> We take a review with rating >=7 as positive and <=4 as negative.  
-> We then make use of the words given in the reviews by looking at their expected index ratio.  
-> We make top 5000 words as attributes for this decision tree learning.  
# Language used
Python  
# Accuracy
-> For Decision Tree  
      95-100%(on training set), 70-77%(on test set)  
-> For Random Forests  
       Maximum of 100% on training and 78.5% on test set  
-> After Pruning  
       78.7% on test set  
# Trade-off between Accuracy and Time
I have given accuracy more preference as compared to time of running of algorithm.  
You can easily reduce the time by using matrix instead of dictionary in the code and it will reduce the time considerably.
   
      
     
