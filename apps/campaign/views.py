from vanilla import TemplateView
from vanilla import FormView


class CenasView(TemplateView):
    """
        Cenas class viiew da cena
        
        **Coisa**
        ``RequestContext``
        
        altamente
    """
    template_name = "base.html"
    
    def get(self, request, *args, **kwargs):
        """
            GET METHOD OVERRIDE CENAS
        
        """
        import celery
        from apps.jobs.tasks import add
	
        res = add.delay(2,5)
        
	

        context = self.get_context_data()
        context["content"] = res.get(timeout=1)
        
        ###
        #TODO: your custom code goes here
        ###
        return self.render_to_response(context)
