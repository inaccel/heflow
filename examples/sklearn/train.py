import click
import heflow.sklearn
import mlflow.sklearn
import sklearn.datasets
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection


@click.command(context_settings={
    'allow_extra_args': True,
    'ignore_unknown_options': True
})
@click.option('--C', default=1.0)
@click.option('--solver', default='lbfgs')
@click.option('--max-iter', default=100)
def train(c, solver, max_iter):
    X, y = sklearn.datasets.fetch_openml('iris', return_X_y=True)

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        X, y, test_size=3, random_state=42)

    mlflow.sklearn.autolog(log_models=False)

    with mlflow.start_run():
        lr = sklearn.linear_model.LogisticRegression(C=c,
                                                     solver=solver,
                                                     max_iter=max_iter)

        model = lr.fit(X_train, y_train)

        predictions = model.predict(X_test)

        print('predictions=%s' % predictions)

        print('accuracy=%.3f' %
              sklearn.metrics.accuracy_score(y_test, predictions))

        heflow.sklearn.log_model(model)


if __name__ == '__main__':
    train()
