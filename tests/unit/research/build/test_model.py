import pytest
from ai_native_workbench.research.build import DeliverySpec, DeliveryType
from ai_native_workbench.research.build.errors import BuildValidationError
def test_delivery_spec_is_immutable_and_freezes_configuration():
    spec=DeliverySpec(DeliveryType.DATASET,'json','p1','r1',{'nested':['x']})
    with pytest.raises(TypeError): spec.configuration['x']=1
    assert spec.configuration['nested']==('x',)
def test_delivery_spec_requires_versions():
    with pytest.raises(BuildValidationError): DeliverySpec(DeliveryType.DATASET,'json','','r',{})
