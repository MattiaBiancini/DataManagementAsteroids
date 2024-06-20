import shap


class Shap:

    def __init__(self, model, x_test, features, tree, num_background_samples=100):
        self.model = model
        self.X_test = x_test

        if tree:
            self.explainer = shap.TreeExplainer(self.model)
            self.shap_values = self.explainer.shap_values(self.X_test)
            self.values_true = self.shap_values[:, :, 0]
        else:
            background = shap.sample(self.X_test, num_background_samples)
            self.explainer = shap.KernelExplainer(self.model, background)
            self.shap_values = self.explainer.shap_values(self.X_test)
            self.values_true = self.shap_values[:, :, 0]

        self.explanation = shap.Explanation(
            values=self.values_true,
            base_values=self.explainer.expected_value,  # Adjust according to your model and explainer
            data=self.X_test,
            feature_names=features
        )

    def waterfall(self, index=0):
        shap.plots.waterfall(self.explanation[index])

    def plot_force(self, index=0):
        shap.initjs()
        display(shap.plots.force(self.explanation[index], matplotlib=False))

    def plot_force_range(self, min=0, max=0):
        shap.initjs()
        display(shap.plots.force(self.explanation[min:max]))

    def plots_bar(self):
        shap.plots.bar(self.explanation)

    def beeswarm(self):
        shap.plots.beeswarm(self.explanation)
